from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from sympy import gcd
import random

# Given values
c = 139720796479374556837839656652540122243007626643381344885901610199769037583634859417560062099728477295868135937894154388536029033912020951046531754291314791576993247093854916427453824336759832613456125812748403327889942337175444534747145584776834634064449332853034222211593992834883804382517469285134615410890552305298817475187104100695214559355963632453798058802239812117081224193187059004755477271402390752746056934083349914720924964985477019671678390124249156133520641131604245493150059531952315986192987567065110493172095513743268697649505813042269117318549842022700777738416504972716492827707238521250172037318878143246460022194896022766776466227648684930789197508257683373695856981117703510481288986657838150127977468181944992384721842001507170848236471999364207702040065244954529595083994706530374178265246266208976848057249872581824068627294869707076024048278537255430854746383501311236149901970358224464288450149417182216604149405350753982608481484751293575534659469072597038338901449655999077721897580555611253838587088501901572616461450861745788408043293875298899352407738097625467580303774153287504872955432866806079131615030274791176371691768412142419959913433427391907036538199289877381635262505011128001699263122593284

hints = [
    3866294283908370861488986000247430995139186777220357990541055308702037903707384419423826283009132248692192568975203597042009355399751936100480421867341262040737335017123404203927518302827224118229709057228844492753128565357229482359457659966763272646136725283420820796129854472327550520891881208553820989688970427173391779160328649128965136830927404708686730062768841805259990187621992590852687212330417117067906587029875088101166137216351257406367577019997777742867451002173150225957848519180489818297384281682372264975637602389081091911467851281502569478148563215408599772010672364892477652656268001246468514425572021865614220946751853939700620295254407108799251461268851704487486728227236288824048447378581527785367882502867237075440070362693035674677027413684269498945804901755587247582322297029281275913387627689148848411252531896135606049738961803492931831122200762928595785709487784007811064183007593040168953263448181,
    3628649695417460562172315261919165549043709593963503335633087846193794925198669443396537711332099330001416771156961283691343877982787723314413110851552024591560420907598588654415705537840898104729737254424204341334008689904573725591551271495102747863837555230824843453350167486014731395948048241691669379097480994057380944391213218649036555692918223032157752111895389190246951731910248198877398965517057737869448282964672470635140939878517426671416232457280765097915904253546503591339765427448900120467971088152395190903792335861055059645334706190248311102008158633420003128537123361250121418756284262680181162625189089585786519534003360535357373023868605497405375065020663001385969284820872120446799517915866964028007422550130397266344718281802740546407102127616395524152153311890940820982444627108375976777379289854717567836101253091116604854859258279919958749154303673140187091899274959707223049802204929874627255009584321,
    9606157182439043598872170578642744168098944919513002317243547092783933349126951101232515925102167428847229467444361689353623296746504025201764596226132219569258571256816498179375058698409595725396407373236481359252082807579175910455629819860184585401808660079698789414010432185309643969322080617826789972798109957,
    557390968116917607877829363093351805079737673251666125750855204507413143402951042823589767603012181329596501910433247254505703477712968699181752906601465941540893134510615975805428225313640362942516617107041546995371614895479364609820877616901492313825956284172514668995110591266769649498902747148214078714361551166533172720774906405292701625129746765757548911894868677588736464297617260842519992821649964146119541180510262047270950140275778830315152105356623177230353223220665627777554864341106987045510247473690102764921346736030282675873380368512116665379912859727258422298886737986021254816678486456826454925033239291650047977879536634028717942088022498515363228773843881827937421252602178359071343399447476754491530354384743821399856731847364080918633699509079462675749036708735344238989499995166818428663564724371054125511464923830553161827722791228424768893864021380022160450622251556525653648961057653640220274868294955432391214814287172091578650091455077186852210252878989421136057443331549592837248178676355257735098257090256064693810738952500512964294218575884615185180922564391962479167159265600516644421242874922033475612568848455701469155055417915197274344345456557389536486925426130886732646054713022908914774519923852,
    538263264876077354278835844354365458289003736282580004677054552128799960628133201065342466271868332880472151805964559748587163918053898759995342752231465836218320104626514241981994011377537441291270452774317491283444142446329524198946300602994669355591759178978441313629896991014103751735455651944949762938101992757874865050589192612588675706284183796825755239043553260296843847013799071173149845196158533600143774705688501254062922926384860349063522338242622392704689866791927863138061957183884357032233632573654406351976706676481304143492464965841758188617909329042280820646392853320414528204206157140231060421944635609596250051670571066978639680472476220763605210759768914567896565243036517540789222487566763401584304485285323923448947626816957034490642108407129443007111596952122083030335946605937834876687675148654878527407472636832862085737586505525535611551828909946664736386297959830871761246381437499696168474217839502976413890295875917502613911304032843445910831763019415476699634154284015804165067691742346908709579361770440364434068760983291051680957726423921878988431317731871208086347006281329458475664817947601463446296166082328266979445064485183236719033479429938563313816672596875515581938722831214134371743273301812
]

# Step 1: Recover original primes p and q from the hints
# Each hint is obfuscated with a multiplication by a random 1024-bit prime

def recover_prime(hint, n):
    while True:
        g = gcd(hint, n)
        if g != 1 and g != n:
            return g
        hint = (hint * random.getrandbits(1024)) % n

# Recover p and q
p = recover_prime(hints[0], n)
q = recover_prime(hints[1], n)

# Step 2: Calculate phi(n)
phi_n = (p - 1) * (q - 1)

# Step 3: Recover the private key d
d = inverse(e, phi_n)

# Step 4: Decrypt the ciphertext
m = pow(c, d, n)

# Convert the decrypted message from a long integer to a byte string
flag = long_to_bytes(m)

print(f"The decrypted flag is: {flag.decode('utf-8')}")
