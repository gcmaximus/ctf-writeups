import logging
from volatility3.framework.interfaces import context
import colorama
import os
import re
import yara
from typing import Iterable, Tuple
from colorama import Fore, Style
from datetime import datetime

from volatility3.framework import interfaces, symbols, exceptions, constants
from volatility3.framework import renderers
from volatility3.cli import text_renderer
from volatility3.framework.configuration import requirements
from volatility3.framework.objects import utility
from volatility3.framework.renderers import UnreadableValue, format_hints, conversion
from volatility3.framework.symbols import intermed
from volatility3.framework.symbols.windows.extensions import pe as pp
from volatility3.plugins.windows import (
    pslist,
    vadinfo,
    cmdline,
    modules,
    dlllist,
    handles,
    filescan,
    dumpfiles,
    lnk_analysis,
)

Section_Permission = {
    "WRITE": 0x80000000,
    "READ": 0x40000000,
    "EXECUTE": 0x20000000,
    "(UNINIT_DATA)": 0x00000080,
    "(INIT_DATA)": 0x00000040,
    "(CODE)": 0x00000020,
}
# logging setting
vollog = logging.getLogger(__name__)

# color print
colorama.init()


class Allfind(interfaces.plugins.PluginInterface):
    """memory abnormal detect plugin

    - get_requirements :
        Check plugin's requirements and options

    - check_thread:
        Check Thread in VAD or Kernel or None

    - get_data:
        Get Process PEB, Threads, VAD, PEB/VAD mapped image

    - check_ioc :
        Check malware abnormal detect by IoC

    """

    _required_framework_version = (1, 0, 0)

    @classmethod
    # for plugin's requirements and options -->
    def get_requirements(cls):
        return [
            requirements.TranslationLayerRequirement(
                name="primary",
                description="Memory layer for the kernel",
                architectures=["Intel32", "Intel64"],
            ),
            requirements.SymbolTableRequirement(
                name="nt_symbols", description="Windows kernel symbols"
            ),
            requirements.ListRequirement(
                name="pid",
                element_type=int,
                description="Process IDs to include (all other processes are excluded)",
                optional=True,
            ),
            requirements.ListRequirement(
                name="lv",
                element_type=int,
                description="Scanning Level(1=Max, 2=General), Default=2",
                optional=True,
            ),
            requirements.BooleanRequirement(
                name="dump",
                description="Extract Malicious Memory Region",
                default=False,
                optional=True,
            ),
            requirements.VersionRequirement(  # get process list
                name="pslist", component=pslist.PsList, version=(2, 0, 0)
            ),
            requirements.VersionRequirement(  # get vad information
                name="vadinfo", component=vadinfo.VadInfo, version=(2, 0, 0)
            ),
            requirements.VersionRequirement(  # get process command line
                name="cmdline", component=cmdline.CmdLine, version=(1, 0, 0)
            ),
            requirements.VersionRequirement(  # get kernel modules
                name="modules", component=modules.Modules, version=(1, 0, 0)
            ),
            requirements.VersionRequirement(  # get dlllist modules
                name="dlllist", component=dlllist.DllList, version=(2, 0, 0)
            ),
            requirements.VersionRequirement(  # get handles modules
                name="handles", component=handles.Handles, version=(1, 0, 0)
            ),
            # requirements.VersionRequirement(  # get filescan modules
            #     name="filescan", component=filescan.FileScan, version=(1, 0, 0)
            # ),
            # requirements.VersionRequirement(  # get handles modules
            #     name="dumpfiles", component=dumpfiles.DumpFiles, version=(1, 0, 0)
            # ),
        ]

    @classmethod
    def dump_vad(self, context, proc, vad):
        file_output = "Error outputting to file"
        try:
            file_handle = vadinfo.VadInfo.vad_dump(context, proc, vad, self.open, maxsize=0)
            file_handle.close()
            file_output = file_handle.preferred_filename
        except (exceptions.InvalidAddressException, OverflowError) as excp:
            vollog.debug(
                "Unable to dump PE with pid {0}.{1:#x}: {2}".format(
                    proc.UniqueProcessId, vad.get_start(), excp
                )
            )
        return file_output

    # <-- end for plugin's requirements and options

    # for executable object -->
    @classmethod
    def get_peb_obj(cls, context, symbol_table, proc_layer_name, proc):
        peb = context.object(
            symbol_table + constants.BANG + "_PEB", layer_name=proc_layer_name, offset=proc.Peb
        )
        return peb

    @classmethod
    def get_pe_table_name(cls, context):
        pe_table_name = intermed.IntermediateSymbolTable.create(
            context, "plugins.PsList", "windows", "pe", class_types=pp.class_types
        )
        return pe_table_name

    @classmethod
    def get_module_pe(cls, context, pe_table_name, mod_data, mod_offset, mod_layer_name):
        if (mod_data != None) and (mod_data[:2] == b"MZ"):
            try:
                module_pe = context.object(
                    pe_table_name + constants.BANG + "_IMAGE_DOS_HEADER",
                    offset=mod_offset,
                    layer_name=mod_layer_name,
                )
                return module_pe
            except exceptions.PagedInvalidAddressException as excp:
                return None

    # <-- end for executable object

    # for process -->
    @classmethod
    def get_proc_id_and_layer(cls, proc):
        proc_id = "Unknown"

        try:
            proc_id = proc.UniqueProcessId
            proc_layer_name = proc.add_process_layer()
        except:
            pass
        return proc_id, proc_layer_name

    @classmethod
    def get_proc_architecture(cls, is_32bit_arch, proc):
        if is_32bit_arch or proc.get_is_wow64():
            architecture = "intel"
        else:
            architecture = "intel64"
        return architecture

    @classmethod
    def get_proc_cmd_arg(cls, context, symbol_table, proc):
        cmd_arg = "-"
        try:
            cmd_arg = cmdline.CmdLine.get_cmdline(context, symbol_table, proc)
        except:
            pass

        return cmd_arg

    @classmethod
    def get_proc_ldr_modules(self, proc):
        proc_env = proc.environment_variables()
        ldr_modules = []
        proc_exe_check_flag = False
        proc_FullName = "-"
        # get proc ldr modules
        for entry in proc.load_order_modules():
            FullDllName = "-"

            try:
                FullDllName = entry.FullDllName.get_string().lower()
            except exceptions.InvalidAddressException:
                continue

            # change env value and store ldr_modules
            for env, var in proc_env:
                if (FullDllName.startswith("\\")) and (FullDllName.split("\\")[1] == env.lower()):
                    FullDllName = "\\".join(
                        FullDllName.replace(FullDllName.split("\\")[1], var.lower()).split("\\")
                    )[1:]
                else:
                    continue
            if len(FullDllName) > 7:  # at least c:\\[.ext]
                try:
                    if entry.LoadReason == 0x4 and entry.ObsoleteLoadCount == 0x6:
                        FullDllName += Fore.YELLOW + " (By LoadLibrary)" + Fore.GREEN
                except:
                    pass
                ldr_modules.append(FullDllName)
            ext = os.path.splitext(FullDllName)[1]

            if ext == ".exe" and proc_exe_check_flag == False:
                proc_FullName = FullDllName.split(":")[1]
                proc_exe_check_flag = True
        return ldr_modules, proc_FullName

    @classmethod
    def get_proc_vads(cls, proc):
        proc_vads = []
        for vad in proc.get_vad_root().traverse():
            proc_vads.append(vad)
        return proc_vads

    # <-- end for process

    # for thread -->
    @classmethod
    def get_thread_for_proc(cls, symbol_table, proc):
        thread_list = []
        for thread in proc.ThreadListHead.to_list(
            symbol_table + constants.BANG + "_ETHREAD", "ThreadListEntry"
        ):
            thread_list.append(thread)
        return thread_list

    @classmethod
    def get_kernel_modules(self, context, layer_name, symbol_table):
        kernel_modules = {}

        for module in modules.Modules.list_modules(context, layer_name, symbol_table):
            module_name = module.FullDllName.get_string().lower()

            kernel_modules[module_name] = {
                "StartAddr": module.DllBase,
                "EndAddr": module.DllBase + module.SizeOfImage,
            }
        return kernel_modules

    @classmethod
    def check_in_kernel_module_range(cls, kernel_modules, thread):
        for module_name in kernel_modules.keys():
            module_start_addr = kernel_modules[module_name]["StartAddr"]
            module_end_addr = kernel_modules[module_name]["EndAddr"]

            if module_start_addr <= thread.Win32StartAddress <= module_end_addr:
                return module_name

    @classmethod
    def check_jmp_kernel(cls, kernel_modules, addr):
        for module_name in kernel_modules.keys():
            module_start_addr = kernel_modules[module_name]["StartAddr"]
            module_end_addr = kernel_modules[module_name]["EndAddr"]

            if module_start_addr <= addr <= module_end_addr:
                return module_name

    @classmethod
    def check_in_vad_range(cls, proc_vads, thread):
        for vad in proc_vads:
            if vad.get_start() <= thread.Win32StartAddress <= vad.get_end():
                return vad

    @classmethod
    def check_jmp_vad(cls, proc_vads, addr):
        for vad in proc_vads:
            if vad.get_start() <= addr <= vad.get_end():
                return vad

    @classmethod
    def check_jmp(cls, disasm_data):
        # First check - if there is a jmp to an address
        jmp_list_to_addr = re.findall("\s*(?:call|jmp)\s*(0x[0-9a-f]+)\s*\n\s*", disasm_data, re.I)

        # Second check - if there is a move and then jmp or call to the register
        jmp_list_to_register = re.findall(
            "(0x[0-9a-f]+)\n0x[0-9a-f]+\s*[0-9a-f]+\s*(?:call|jmp)\s*[a-z]+\n",
            disasm_data,
            re.I,
        )

        return jmp_list_to_addr + jmp_list_to_register

    @classmethod
    def thread_valid_check(cls, thread):
        # valid check (some thread_list[-1] is error / maybe volatility3 error  )
        try:
            if thread.Cid.UniqueThread < 65535:
                return True
        except:
            return False
        return False

    # <-- end for thread

    # for vad -->

    @classmethod
    def check_vadFlags(cls, vad):
        if vad.has_member("u"):
            vad_type = vad.u.VadFlags.VadType
        elif vad.has_member("Core"):
            vad_type = vad.Core.u.VadFlags.VadType

        if vad_type == 2:  # IMAGE_FILE_TYPE
            return True
        else:
            return False

    @classmethod
    def get_vad_file_object(cls, vad):
        vad_file_object = None

        try:
            vad_file_object = vad.Subsection.ControlArea.FilePointer.dereference().cast(
                "_FILE_OBJECT"
            )
        except:
            pass

        return vad_file_object

    @classmethod
    def get_vad_protection(cls, context, proc_layer_name, symbol_table, vad):
        vad_protection = None
        try:
            vad_protection = vad.get_protection(
                vadinfo.VadInfo.protect_values(context, proc_layer_name, symbol_table),
                vadinfo.winnt_protections,
            )
        except:
            pass

        return vad_protection

    @classmethod
    def yarcallback(cls, data):
        if data["matches"] == True:
            print(data)

        yara.CALLBACK_CONTINUE

    # <-- end for vad

    # print -->
    @classmethod
    def print_proc_info(cls, process_name, proc, architecture, cmd_arg):
        print(
            "\n\n"
            + Fore.CYAN
            + "{0} | PID : {1} | PPID : {2} | Threads : {3} | Arch : {4} | {5}".format(
                process_name,
                proc.UniqueProcessId,
                proc.InheritedFromUniqueProcessId,
                proc.ActiveThreads,
                architecture,
                cmd_arg,
            )
            + Style.RESET_ALL
        )

    @classmethod
    def print_ldr_modules(cls, ldr_modules):
        print(
            "\n"
            + Fore.GREEN
            + "Ldr Modules : \t{0}".format("\n\t\t".join(ldr_modules))
            + Style.RESET_ALL
            + "\n\n  {0:<14} {1:>14} | {2:^10} | {3:^33} | {4:^4} | {5}".format(
                "VOffset",
                "VSize",
                "Tag",
                "Protection",
                "Commit",
                "FileName",
            )
        )

    @classmethod
    def print_no_location_thread(cls, thread):
        print(
            Fore.RED
            + "TID {0:^6} | Thread Address : {1:>14} | No Location / Unmmaped(?)".format(
                thread.Cid.UniqueThread,
                hex(thread.Win32StartAddress),
            )
            + Style.RESET_ALL
        )

    @classmethod
    def print_at_kernel_thread(cls, thread, at_kernel_module_thread_name):
        print(
            Fore.YELLOW
            + "TID {0:^6} | Thread Address : {1:>14} | KernelModule {2}".format(
                thread.Cid.UniqueThread,
                hex(thread.Win32StartAddress),
                at_kernel_module_thread_name,
            )
            + Style.RESET_ALL
        )

    @classmethod
    def print_pe_section(cla, section):
        print("\n")
        for key in section.keys():
            print(
                "{0:<14} {1:.>14} | {2:^10} | {3}".format(
                    hex(section[key]["VAddr"]),
                    hex(section[key]["Size"]),
                    key,
                    section[key]["Permission"],
                )
            )

    @classmethod
    def print_result(
        cls, desc, vad, vad_protection, vad_FullName, disasm_data, vad_data, point, point_color
    ):
        print(
            point_color
            + "[MalPoint] : {0:<4}\t".format(point)
            + desc
            + "\n->"
            + Fore.WHITE
            + "{0:>14} {1:.>14} | {2:^10} | {3:^33} | {4:^3} | {5} \nHex: {6} \nEntry Dissasm :{7}".format(  # \n {6}".format(
                hex(vad.get_start()),
                hex(vad.get_end() - vad.get_start() + 1),
                vad.get_tag(),
                vad_protection,
                vad.get_commit_charge(),
                vad_FullName,
                Fore.BLUE + str(vad_data) + Fore.WHITE,
                disasm_data,
            )
            + Style.RESET_ALL
        )

    # <-- end print

    """
    main method start
    """
    # for delete lnk files
    def cleanup(cls):
        target = os.listdir(os.getcwd())

        for del_file in target:
            if del_file.endswith(".dat"):
                os.remove(os.path.join(os.getcwd(), del_file))
            elif del_file.startswith("tmp_"):
                os.remove(os.path.join(os.getcwd(), del_file))

    # for related proc
    def check_sus_proc(self, target_proc_c_time, proc_array):
        for proc in proc_array:
            matche_living = match_filelss = None
            diff_sec = (target_proc_c_time - proc["proc_c_time"]).seconds
            rules_living = re.compile(
                "powershell.exe|cscript.exe|cmd.exe|wscript.exe|vbscript.exe|mshta.exe|.ps1|.vbs|bitsadmin.exe|certutil.exe|control.exe|esentutl.exe|expand.exe|extrac32.exe|findstr.exe|forfiles.exe|makecab.exe|mavinject.exe|mpcmdrun.exe|print.exe|reg.exe|regedit.exe|regini.exe|rundll32.exe|runonce.exe|sc.exe|schtasks.exe|wmic.exe|xwizard.exe|appinstaller.exe|at.exe|atbroker.exe"
            )
            matche_living = rules_living.search(str(proc["proc_name"]).lower())
            rules_fileless = re.compile(".xls|.ppt|.doc|.xlsx|.pptx|.docx|.js|.lnk")
            match_filelss = rules_fileless.search(str(proc["cmd"]).lower())

            if diff_sec < 60 and diff_sec > 0:
                if proc["cmd"] == "-":
                    cmd_text = (
                        proc["proc_name"] + Fore.YELLOW + " May Be Exited(?)" + Style.RESET_ALL
                    )
                else:
                    cmd_text = proc["cmd"]
                if matche_living != None:
                    print(
                        Fore.YELLOW
                        + "\nSuspicious Process : "
                        + Fore.RED
                        + "\n- PID : {0}".format(proc["pid"])
                        + Style.RESET_ALL
                        + " {0}".format(cmd_text)
                    )

                elif match_filelss != None:
                    print(
                        Fore.YELLOW
                        + "\nSuspicious File Execute Cmd : "
                        + Fore.RED
                        + "\n- PID : {0}".format(proc["pid"])
                        + Style.RESET_ALL
                        + " {0}".format(proc["cmd"])
                    )

    # for related file
    def check_sus_file(self, lnk_array, proc_c_time):
        type_print = ""
        for entry in lnk_array:
            tgt_atime = datetime.strptime(entry["tgt_atime"], "%Y-%m-%d %H:%M:%S")
            diff_sec = (proc_c_time - tgt_atime).seconds
            if diff_sec < 300:  # 5minute
                if entry["type"].find("DIRECTORY") > 0:
                    type_print = "Suspicious Folder"
                else:
                    type_print = "Suspicious File"

                print(
                    Fore.YELLOW
                    + "\n{0} : {1:<25}".format(type_print, entry["path"])
                    + Style.RESET_ALL
                    + "\n- Executed {0}, {1} second difference(from Process Start Time)".format(
                        tgt_atime, diff_sec
                    )
                )

    # for persist
    def check_persist(self, vad, proc_layer):
        try:
            vad_read_data = proc_layer.read(
                vad.get_start(), vad.get_end() - vad.get_start() + 1, pad=True
            )
        except:
            vad_read_data = "\x00"  # memory read error

        rules = yara.compile(filepath="./volatility3/framework/plugins/windows/liv.yar")

        matches = 0
        matches = rules.match(data=vad_read_data, callback=self.yarcallback)
        if len(matches) > 0 and str(matches).find("living") > 0:
            # point += 10
            print(Fore.RED + "Living Find\t " + Style.RESET_ALL)

    # get lnk files
    def get_files(self, context, layer_name, symbol_table):
        lnk_array = []
        for fileobj in filescan.FileScan.scan_files(context, layer_name, symbol_table):
            try:
                file_name = fileobj.FileName.String

                if file_name[-3:] == "lnk":
                    temp_file = dumpfiles.DumpFiles.process_file_object(
                        context, layer_name, self.open, fileobj
                    )

                    for lnk in temp_file:
                        if len(lnk) == 4 and lnk[3].find("Error") < 0:
                            path = lnk[3]
                            file = open(path, "rb")
                            lnk_data = lnk_analysis.LnkAnalysis(file, path).get_all_info()[0]
                            lnk_array.append(
                                {
                                    "lnk_fname": lnk[2],
                                    "path": lnk_data["Localbasepath"],
                                    "type": lnk_data["File Attributes0"],
                                    "tgt_ctime": lnk_data["Target File Creation Time"],
                                    "tgt_atime": lnk_data["Target File Access Time"],
                                }
                            )
                            file.close()
                            os.remove(path)
                        else:
                            break
                    temp_file.close()
                    os.remove(temp_file)
            except:
                continue
        return lnk_array

    # for handles
    def get_handles(self, proc, context, layer_name, symbol_table):
        handles_plugin = handles.Handles(context, self.config_path)
        type_map = handles_plugin.get_type_map(context, layer_name, symbol_table)
        cookie = handles_plugin.find_cookie(context, layer_name, symbol_table)
        reg_array = []
        file_array = []

        try:
            object_table = proc.ObjectTable
        except exceptions.InvalidAddressException:
            return

        for entry in handles_plugin.handles(object_table):
            try:
                obj_type = entry.get_object_type(type_map, cookie)
                if obj_type == "Key":
                    item = entry.Body.cast("_CM_KEY_BODY")
                    obj_name = item.get_full_key_name()
                    reg_array.append(obj_name)
                elif obj_type == "File":
                    item = entry.Body.cast("_FILE_OBJECT")
                    obj_name = item.file_name_with_device()
                    if type(obj_name) == str:
                        file_array.append(obj_name)
            except:
                continue

        return reg_array, file_array

    # Check Thread in VAD or Kernel or None
    def check_thread_range(self, thread_list, proc_vads, kernel_modules, level):
        seen_thread = {}
        for thread in thread_list:
            if self.thread_valid_check(thread) == False:
                continue
            vad_has_thread = None
            at_kernel_module_thread_name = None

            vad_has_thread = self.check_in_vad_range(proc_vads, thread)

            if vad_has_thread == None:

                at_kernel_module_thread_name = self.check_in_kernel_module_range(
                    kernel_modules, thread
                )

                if at_kernel_module_thread_name == None:
                    self.print_no_location_thread(thread)

                else:
                    if level == 1:
                        self.print_at_kernel_thread(thread, at_kernel_module_thread_name)
                    else:
                        pass

            else:
                seen_thread[vad_has_thread.get_start()] = {
                    "vad": vad_has_thread,
                    "thread": thread,
                }
        return seen_thread

    def check_pe(self, vad, vad_pe, proc_layer, architecture, point, desc, section, sec_flag):
        pe_entry = (
            vad_pe.get_nt_header().OptionalHeader.ImageBase
            + vad_pe.get_nt_header().OptionalHeader.AddressOfEntryPoint
        )
        entry_data = proc_layer.read(pe_entry, 16, pad=True)

        sec_point = 0
        sec_permission = sec_desc = ""
        sec_total = sec_permission_cnt = sec_exectable_cnt = 0
        entry_in_sec = entry_in_code = False

        entry_diss = interfaces.renderers.Disassembly(entry_data, pe_entry, architecture)
        disasm_data = text_renderer.display_disassembly(entry_diss)

        for sec in vad_pe.get_nt_header().get_sections():
            sec_total += sec.SizeOfRawData
            sec_name = utility.array_to_string(sec.Name)
            # section permission check
            for n, v in Section_Permission.items():
                if sec.Characteristics & v != 0:
                    sec_permission += n + " "

            section[sec_name] = {
                "VAddr": vad.get_start() + sec.VirtualAddress,
                "Size": sec.SizeOfRawData,
                "Permission": sec_permission,
            }
            sec_permission = ""

            # section EXECUTABLE but not Code
            if (sec.Characteristics & 0x20000000 != 0) and (sec.Characteristics & 0x00000020 == 0):
                sec_permission_cnt += 1

            # EXECUTABLE Section Not Found
            if sec.Characteristics & 0x20000000 != 0:
                sec_exectable_cnt += 1
                # Entry in Code Section
                if (
                    (vad.get_start() + sec.VirtualAddress)
                    < pe_entry
                    < (vad.get_start() + sec.VirtualAddress + sec.SizeOfRawData)
                ):
                    entry_in_code = True

            # pe_entry not in Section Range
            if (
                (vad.get_start() + sec.VirtualAddress)
                < pe_entry
                < (vad.get_start() + sec.VirtualAddress + sec.SizeOfRawData)
            ):
                entry_in_sec = True

        # 1. check pe_size < sec_total
        pe_size = vad_pe.get_nt_header().OptionalHeader.SizeOfImage
        if pe_size < sec_total:
            sec_point += 10
            sec_desc += Fore.RED + "Section Malformed\t" + Style.RESET_ALL

        # 2. section EXECUTABLE but not Code
        if sec_permission_cnt > 1:
            sec_point += sec_permission_cnt * 5
            sec_desc += Fore.YELLOW + "X Permission in None code section\t" + Style.RESET_ALL

        # 3. EXECUTABLE Section Not Found
        if sec_exectable_cnt < 1:
            sec_point += 2
            sec_desc += Fore.YELLOW + "Executable Section Not Found\t" + Style.RESET_ALL

        # 4. pe_entry not in Section Range
        if entry_in_sec == False:
            sec_point += 2
            sec_desc += (
                Fore.YELLOW + "Entry {0} not in Section\t".format(hex(pe_entry)) + Style.RESET_ALL
            )

        # 5. pe entry not in Code Section
        if (entry_in_sec == True) and (entry_in_code == False):
            sec_point += 2
            sec_desc += Fore.YELLOW + "Entry not in Code Section\t" + Style.RESET_ALL

        # 6. DataDirectory Not 16
        if vad_pe.get_nt_header().OptionalHeader.DataDirectory.count != 16:
            sec_point += 10
            sec_desc += Fore.RED + "DataDirectory Malformed\t" + Style.RESET_ALL

        # Add Point and Description
        if (sec_point / 10) > 1 and len(sec_desc) > 0:
            sec_flag = True
            desc += sec_desc
            point += sec_point

        return disasm_data, point, desc, sec_flag, section

    # Get Process PEB, VAD, PEB/VAD mapped image
    def get_data(
        self, context, symbol_table, proc, proc_layer_name, proc_layer
    ) -> Iterable[Tuple[interfaces.objects.ObjectInterface, bytes]]:

        if proc.Peb:  # normal process must have peb
            # get process _PEB object
            peb = self.get_peb_obj(context, symbol_table, proc_layer_name, proc)

            # get process pe (mapped image)
            pe_table_name = self.get_pe_table_name(context)
            try:
                proc_data = proc_layer.read(peb.ImageBaseAddress, 16, pad=True)
            except:
                return
            proc_pe = self.get_module_pe(
                context, pe_table_name, proc_data, peb.ImageBaseAddress, proc_layer_name
            )

            # peb.ImageBaseAddress, proc_layer_name
            for vad in proc.get_vad_root().traverse():

                vad_data = proc_layer.read(vad.get_start(), 16, pad=True)
                # get vad pe (mapped image)
                vad_pe = self.get_module_pe(
                    context, pe_table_name, vad_data, vad.get_start(), proc_layer_name
                )

                # get vad _FILE_OBJECT
                vad_file_object = self.get_vad_file_object(vad)

                # get vad protecetion
                vad_protection = self.get_vad_protection(
                    context, proc_layer_name, symbol_table, vad
                )

                yield proc_layer, peb, proc_pe, vad, vad_data, vad_pe, vad_file_object, vad_protection

    # Check malware abnormal detect by IoC
    def check_ioc(
        self,
        proc,
        peb,
        proc_layer,
        proc_pe,
        proc_vads,
        vad,
        vad_data,
        vad_pe,
        vad_file_object,
        vad_protection,
        proc_FullName,
        ldr_modules,
        seen_thread,
        architecture,
        kernel_modules,
    ):
        vad_FullName = "-"
        point = 0
        desc = desc_temp = ""
        mapped_image_flag = self.check_vadFlags(vad)
        vad_has_thread = False
        thread_disasm_data = None
        disasm_data = entry_diss = ""
        tid = ""
        section = {}
        sec_flag = False
        malfind_flag = False

        # check vad has thread
        for vad_start_addr in seen_thread.keys():
            if vad.get_start() == vad_start_addr:
                vad_has_thread = True

        # thread (in vad) check : check 4 ioc
        if vad_has_thread == True:
            # 1. thread not have mapped image
            if mapped_image_flag == False:
                point += 10
                desc += Fore.RED + "Thread not have mapped image\t" + Style.RESET_ALL

            thread = seen_thread[vad.get_start()]["thread"]

            # 2. thread PID and Process PID not matched
            if proc.UniqueProcessId != thread.Cid.UniqueProcess:
                desc += Fore.RED + "Thread PID != Process PID\t" + Style.RESET_ALL

            tid = (
                Fore.LIGHTGREEN_EX
                + "TID : {0:^6} \t".format(thread.Cid.UniqueThread)
                + Style.RESET_ALL
            )

            # get thread data
            try:
                thread_data = proc_layer.read(thread.Win32StartAddress, 16, pad=True)
            except:
                thread_data = False

            wait_reason = int(thread.Tcb.WaitReason)
            state = int(thread.Tcb.State)

            # 3. suspended thread check
            if state == 5 and wait_reason == 5:
                point += 5
                desc += Fore.YELLOW + "Thread Suspended\t" + Style.RESET_ALL

            if thread_data != False:
                thread_disasm = interfaces.renderers.Disassembly(
                    thread_data, thread.Win32StartAddress, architecture
                )
                thread_disasm_data = text_renderer.display_disassembly(thread_disasm)

                # 4. thread jump check
                jmp_list = self.check_jmp(thread_disasm_data)

                if jmp_list:
                    for addr in jmp_list:
                        if not addr:
                            continue
                        addr = int(addr, 16)

                        if vad.get_start() <= addr <= vad.get_end():
                            continue
                        else:
                            jmp_vad = self.check_jmp_vad(proc_vads, addr)

                            if jmp_vad:
                                if vad.get_private_memory() == 1:
                                    point += 10
                                    desc += (
                                        Fore.RED
                                        + "Jump to another vad {0} (PRIVATE)\t".format(
                                            hex(jmp_vad.get_start())
                                        )
                                        + Style.RESET_ALL
                                    )
                                else:
                                    point += 7
                                    desc += (
                                        Fore.RED
                                        + "Jump to another vad {0} But Not PRIVATE\t".format(
                                            hex(jmp_vad.get_start())
                                        )
                                        + Style.RESET_ALL
                                    )
                            else:
                                jmp_kernel = self.check_jmp_kernel(kernel_modules, addr)
                                if jmp_kernel:
                                    point += 5
                                    desc += (
                                        Fore.YELLOW
                                        + "Jump to Kernel Module {0}\t".format(jmp_kernel)
                                        + Style.RESET_ALL
                                    )
                                else:
                                    point += 5
                                    desc += (
                                        Fore.YELLOW
                                        + "Couldn't find Jmp Location {0}\t".format(addr)
                                        + Style.RESET_ALL
                                    )

        # vad_protection exist : check 1 ioc
        if vad_protection != None:
            # 1. execute & write it may be shellcode
            if (
                ("EXECUTE" in vad_protection)
                and ("WRITE" in vad_protection)
                and (vad.get_private_memory() == True)
                and (vad.get_commit_charge() != 0)
            ):
                point += 5
                desc += Fore.YELLOW + "EXECUTE & WRITE Possible VAD" + "\t" + Style.RESET_ALL
                malfind_flag = True

        # mapped image exist : check 5 ioc
        try:
            vad_pe.get_nt_header()
        except:
            vad_pe = None

        if vad_pe != None:
            # 1. VAD _FILE_OBJECT check
            if vad_file_object == None:
                point += 10
                desc += Fore.RED + "VAD FILE_OBJECT Not Found\t" + Style.RESET_ALL
                desc += Fore.LIGHTMAGENTA_EX + "Suspicious PE Image Detected\t" + Style.RESET_ALL
            elif vad_file_object != None:
                # 2. Injected Dll check
                if (
                    vad.Subsection.ControlArea.NumberOfMappedViews == 0x1
                    and vad.Subsection.ControlArea.NumberOfUserReferences == 0x1
                    and "EXECUTE" in vad_protection
                    and "WRITE" in vad_protection
                ):
                    point += 2
                    desc += Fore.LIGHTBLACK_EX + "Maybe Dll Injected" + "\t" + Style.RESET_ALL

                # 3. missing PEB check
                try:
                    vad_FullName = vad_file_object.FileName.String.lower()
                except:
                    vad_FulllName = "Not Readable"
                if ((vad_FullName in " ".join(ldr_modules)) == False) and (
                    (os.path.splitext(vad_FullName)[1] == ".exe")
                    or (os.path.splitext(vad_FullName)[1] == ".dll")
                ):
                    point += 2
                    desc += Fore.LIGHTBLACK_EX + "Not in PEB Loaded Module" + "\t" + Style.RESET_ALL
                # 4. check pe malformed
                entry_diss, point, desc, sec_flag, section = self.check_pe(
                    vad,
                    vad_pe,
                    proc_layer,
                    architecture,
                    point,
                    desc,
                    section,
                    sec_flag,
                )
            # 5. vad has malicious shellcode or ReflectiveDll Func
            if malfind_flag == True:
                try:
                    data = proc_layer.read(
                        vad.get_start(), vad.get_end() - vad.get_start() + 1, pad=True
                    )
                except:
                    data = "\x00"  # memory read error

                rules = yara.compile(
                    filepath="./volatility3/framework/plugins/windows/shell_refdll.yar"
                )
                hash_detected = 0
                matches = 0

                loadlibrary = data.find(b"\x8E\x4e\x0e\xec")
                kernel32 = data.find(b"\x5b\xbc\x4a\x6a")
                ntdll = data.find(b"\x5d\x68\xfa\x3c")
                GETPROCADDRESS_HASH = data.find(b"\xAA\xfc\x0d\x7c")
                VIRTUALALLOC_HASH = data.find(b"\x54\xca\xaf\x91")
                NTFLUSHINSTRUCTIONCACHE_HASH = data.find(b"\xB8\x0a\x4c\x53")

                if loadlibrary > 0:
                    hash_detected += 1
                if kernel32 > 0:
                    hash_detected += 1
                if ntdll > 0:
                    hash_detected += 1
                if GETPROCADDRESS_HASH > 0:
                    hash_detected += 1
                if VIRTUALALLOC_HASH > 0:
                    hash_detected += 1
                if NTFLUSHINSTRUCTIONCACHE_HASH > 0:
                    hash_detected += 1

                matches = rules.match(data=data)

                if hash_detected >= 6 and len(matches) > 0:
                    point += 10
                    desc += Fore.RED + "Reflective DLL Injection\t" + Style.RESET_ALL
                elif hash_detected < 6 and len(matches) > 0:
                    point += 10
                    if str(matches).find("shell") > 0:
                        desc += Fore.RED + "Shellcode Find\t " + Style.RESET_ALL

        # get disasm data : 2way, vad or thread
        if (
            (thread_disasm_data == None)
            and (vad_data != None)
            and (vad_pe != None)
            and (vad_file_object != None)
        ):
            disasm_data = entry_diss
        elif (thread_disasm_data == None) and (vad_data != None):
            vad_disasm = interfaces.renderers.Disassembly(vad_data, vad.get_start(), architecture)
            disasm_data = text_renderer.display_disassembly(vad_disasm)
        elif thread_disasm_data != None:
            disasm_data = thread_disasm_data
        else:
            disasm_data = ""

        # process check (vad_pe and proc_pe must exist) : check 2 ioc
        if (
            (mapped_image_flag == True)
            and (proc_pe != None and len(proc_FullName) > 0)
            and (os.path.splitext(vad_FullName)[1] == ".exe")
        ):
            if vad.get_start() == peb.ImageBaseAddress:
                # 1. check PEB Path and Mapped Image Path
                if vad_FullName != proc_FullName:
                    point += 10
                    desc += (
                        Fore.RED + "PEB and Mapped Image Location Mismatch" + "\t" + Style.RESET_ALL
                    )

                else:
                    desc_temp += Fore.GREEN + "PEB and Mapped Image Normal" + "\t" + Style.RESET_ALL

            # 2. check PEB and Mapped Image Base
            elif vad.get_start() != peb.ImageBaseAddress:
                point += 10
                desc += Fore.RED + "PEB and Mapped Image Base Mismatch" + "\t" + Style.RESET_ALL

        # if suspicious detected!! TID print add
        if len(desc) > 0:
            desc = tid + desc

        return desc, vad_FullName, point, disasm_data, sec_flag, section

    def _generator(self, procs):
        lnk_array = proc_array = []
        layer_name = self.config["primary"]
        symbol_table = self.config["nt_symbols"]

        # determine 32 or 64 bit kernel
        is_32bit_arch = not symbols.symbol_table_is_64bit(self.context, symbol_table)

        # get kernel modules for thread address range check
        kernel_modules = self.get_kernel_modules(self.context, layer_name, symbol_table)

        # get level
        if self.config["lv"]:
            level = self.config.get("lv")[0]
        else:
            level = 2

        # get lnk
        if level == 1:
            lnk_array = self.get_files(self.context, layer_name, symbol_table)

        # get process array
        for_array_plist = pslist.PsList.list_processes(
            context=self.context,
            layer_name=self.config["primary"],
            symbol_table=self.config["nt_symbols"],
        )
        for proc in for_array_plist:
            process_name = "-"
            cmd_arg = "-"
            proc_c_time = ""
            proc_id, proc_layer_name = self.get_proc_id_and_layer(proc)
            process_name = utility.array_to_string(proc.ImageFileName)
            cmd_arg = self.get_proc_cmd_arg(self.context, symbol_table, proc)
            proc_c_time = proc.get_create_time()

            # make process array
            proc_array.append(
                {
                    "pid": proc_id,
                    "proc_name": process_name,
                    "proc_c_time": proc_c_time,
                    "cmd": cmd_arg,
                }
            )

        # check each process
        for proc in procs:
            proc_flag = False
            proc_id, proc_layer_name = self.get_proc_id_and_layer(proc)
            proc_layer = self.context.layers[proc_layer_name]
            process_name = utility.array_to_string(proc.ImageFileName)
            proc_c_time = proc.get_create_time()

            # ignore WindowsDefender & MemCompression
            ignore_list = ["MsMpEng.exe", "MemCompression", "System", "Registry"]
            if process_name in ignore_list:
                continue

            # get process architecture
            architecture = self.get_proc_architecture(is_32bit_arch, proc)

            # get process full path and arguments
            cmd_arg = self.get_proc_cmd_arg(self.context, symbol_table, proc)

            # print process default information
            self.print_proc_info(process_name, proc, architecture, cmd_arg)

            # get process loading modules
            ldr_modules, proc_FullName = self.get_proc_ldr_modules(proc)

            # print process loading modules and column names
            if level == 1:
                self.print_ldr_modules(ldr_modules)

            # get process vads
            proc_vads = self.get_proc_vads(proc)

            # get process all thread list
            thread_list = self.get_thread_for_proc(symbol_table, proc)

            # check thread range and vad has thread list
            seen_thread = self.check_thread_range(thread_list, proc_vads, kernel_modules, level)

            # get process all handle list
            reg_list, file_list = self.get_handles(proc, self.context, layer_name, symbol_table)

            # get data for check IoC (vad level check)
            for (
                proc_layer,
                peb,
                proc_pe,
                vad,
                vad_data,
                vad_pe,
                vad_file_object,
                vad_protection,
            ) in self.get_data(self.context, symbol_table, proc, proc_layer_name, proc_layer):
                sec_flag = False
                section = {}

                # Dump options
                file_output = "Disabled"
                if self.config['dump']:
                    file_output = "Error outputting to file"
                    try:
                        file_handle = vadinfo.VadInfo.vad_dump(self.context, proc, vad, self.open)
                        file_handle.close()
                        file_output = file_handle.preferred_filename
                    except (exceptions.InvalidAddressException, OverflowError) as excp:
                        vollog.debug("Unable to dump PE with pid {0}.{1:#x}: {2}".format(
                            proc.UniqueProcessId, vad.get_start(), excp))

                # check persist
                # self.check_persist(vad, proc_layer)  ## miss

                # check ioc
                desc, vad_FullName, point, disasm_data, sec_flag, section = self.check_ioc(
                    proc,
                    peb,
                    proc_layer,
                    proc_pe,
                    proc_vads,
                    vad,
                    vad_data,
                    vad_pe,
                    vad_file_object,
                    vad_protection,
                    proc_FullName,
                    ldr_modules,
                    seen_thread,
                    architecture,
                    kernel_modules,
                )

                point_color = None

                if point > 10:
                    point_color = Fore.RED
                elif point <= 10 and point >= 5 and level == 1:
                    point_color = Fore.YELLOW

                # print suspicious information
                if len(desc) > 2 and point_color != None:
                    proc_flag = True
                    self.print_result(
                        desc,
                        vad,
                        vad_protection,
                        vad_FullName,
                        disasm_data,
                        vad_data,
                        point,
                        point_color,
                    )
                else:
                    continue

                if sec_flag == True or (proc_FullName in vad_FullName):
                    self.print_pe_section(section)

                # not use renderers.TreeGrid just for generator
                yield (
                    0,
                    ("",),
                )
            if proc_flag == True:
                print(
                    Fore.YELLOW
                    + "\nAccess REG : \n\t"
                    + Style.RESET_ALL
                    + "- "
                    + "\n\t- ".join(reg_list)
                )
                print(
                    Fore.YELLOW
                    + "\nAccess FILE : \n\t"
                    + Style.RESET_ALL
                    + "- "
                    + "\n\t- ".join(file_list)
                )
                if level == 1:
                    self.check_sus_file(lnk_array, proc_c_time)
                self.check_sus_proc(proc_c_time, proc_array)
                proc_flag = False

        if level == 1:
            self.cleanup()

    def run(self):
        filter_func = pslist.PsList.create_pid_filter(self.config.get("pid", None))

        return renderers.TreeGrid(
            [
                ("Analyze ...", str),
            ],
            self._generator(
                pslist.PsList.list_processes(
                    context=self.context,
                    layer_name=self.config["primary"],
                    symbol_table=self.config["nt_symbols"],
                    filter_func=filter_func,
                )
            ),
        )