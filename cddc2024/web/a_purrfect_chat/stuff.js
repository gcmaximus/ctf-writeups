var yl = He,
	cp = ap;

function fp(e, t) {
	return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t
}
var dp = typeof Object.is == "function" ? Object.is : fp,
	pp = cp.useSyncExternalStore,
	mp = yl.useRef,
	hp = yl.useEffect,
	vp = yl.useMemo,
	yp = yl.useDebugValue;
mc.useSyncExternalStoreWithSelector = function(e, t, n, r, l) {
	var o = mp(null);
	if (o.current === null) {
		var u = {
			hasValue: !1,
			value: null
		};
		o.current = u
	} else u = o.current;
	o = vp(function() {
		function s(g) {
			if (!c) {
				if (c = !0, h = g, g = r(g), l !== void 0 && u.hasValue) {
					var w = u.value;
					if (l(w, g)) return m = w
				}
				return m = g
			}
			if (w = m, dp(h, g)) return w;
			var S = r(g);
			return l !== void 0 && l(w, S) ? w : (h = g, m = S)
		}
		var c = !1,
			h, m, p = n === void 0 ? null : n;
		return [function() {
			return s(t())
		}, p === null ? void 0 : function() {
			return s(p())
		}]
	}, [t, n, r, l]);
	var i = pp(e, o[0], o[1]);
	return hp(function() {
		u.hasValue = !0, u.value = i
	}, [i]), yp(i), i
};
pc.exports = mc;
var gp = pc.exports;
const wp = Bo(gp);
var yc = {
	BASE_URL: "/",
	MODE: "production",
	DEV: !1,
	PROD: !0,
	SSR: !1
};
const {
	useDebugValue: Sp
} = is, {
	useSyncExternalStoreWithSelector: kp
} = wp;
let Gi = !1;
const Ep = e => e;

function xp(e, t = Ep, n) {
	(yc ? "production" : void 0) !== "production" && n && !Gi && (console.warn("[DEPRECATED] Use `createWithEqualityFn` instead of `create` or use `useStoreWithEqualityFn` instead of `useStore`. They can be imported from 'zustand/traditional'. https://github.com/pmndrs/zustand/discussions/1937"), Gi = !0);
	const r = kp(e.subscribe, e.getState, e.getServerState || e.getInitialState, t, n);
	return Sp(r), r
}
const Zi = e => {
		(yc ? "production" : void 0) !== "production" && typeof e != "function" && console.warn("[DEPRECATED] Passing a vanilla store will be unsupported in a future version. Instead use `import { useStore } from 'zustand'`.");
		const t = typeof e == "function" ? bd(e) : e,
			n = (r, l) => xp(t, r, l);
		return Object.assign(n, t), n
	},
	_p = e => e ? Zi(e) : Zi,
	Cp = _p(() => ({
		items: ["10", "11", 0, 1, 2, 3, 18, 176]
	}));

function gc({
	result: e,
	value: t
}) {
	const [n, r] = He.useState("Please input the answer"), l = Cp(i => i.items), o = () => /\)$/.test(t) && t.split("")[7] === l[4].toString() && t.split("")[9].charCodeAt() === parseInt(100 + l[7] % l[6]) && t.slice(11, 13) === "Brilliant".substring(7) && t.split("")[2] === l[3] + "", u = () => t.split("")[15] === "d" && t.split("")[3].charCodeAt() === 99 && t.split("")[14].charCodeAt() === parseFloat(l[1] + l[2]) && t.split("")[10] === "0";
	return He.useEffect(() => {
		e === "o" && t.split("")[16].charCodeAt() === 58 && o() && u() ? r("Correct!") : e === "x" && r("Try again :(")
	}, [e]), Q.jsx("span", {
		className: "bg-white rounded-3xl rounded-bl-none p-4 w-4/5 mt-4 ml-4",
		children: n
	})
}
gc.propTypes = {
	result: Yi.string,
	value: Yi.string
};
const Pp = "/assets/miauu-CRMPhZxe.jpg",
	Np = "data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20512%20512'%3e%3c!--!Font%20Awesome%20Free%206.5.2%20by%20@fontawesome%20-%20https://fontawesome.com%20License%20-%20https://fontawesome.com/license/free%20Copyright%202024%20Fonticons,%20Inc.--%3e%3cpath%20fill='%23969696'%20d='M16.1%20260.2c-22.6%2012.9-20.5%2047.3%203.6%2057.3L160%20376V479.3c0%2018.1%2014.6%2032.7%2032.7%2032.7c9.7%200%2018.9-4.3%2025.1-11.8l62-74.3%20123.9%2051.6c18.9%207.9%2040.8-4.5%2043.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448%20256zm52.1%2025.5L409.7%2090.6%20190.1%20336l1.2%201L68.2%20285.7zM403.3%20425.4L236.7%20355.9%20450.8%20116.6%20403.3%20425.4z'/%3e%3c/svg%3e";

function zp() {
	const [e, t] = He.useState(""), [n, r] = He.useState(""), l = () => {
		e.length === 18 && e.split("")[8].charCodeAt() === parseInt("70") && e.split("")[1].charCodeAt() === 101 && e.split("")[13] === "3" && e.slice(4, -11) === "You are awesome!".substr(-4, 3) && e.split("")[0].charCodeAt() === parseInt(e.split("")[8].charCodeAt()) + 17 ? r("o") : r("x")
	};
	return Q.jsxs("div", {
		className: "rounded-xl bg-gray-300 w-2/3 h-[500px] flex flex-col gap-4",
		children: [Q.jsxs("div", {
			className: "flex gap-4 items-center pt-7 pl-7",
			children: [Q.jsx("div", {
				className: "rounded-full overflow-hidden w-20",
				children: Q.jsx("img", {
					src: Pp,
					className: "w-full h-full"
				})
			}), Q.jsxs("div", {
				children: [Q.jsx("p", {
					className: "font-bold",
					children: "Cat"
				}), Q.jsx("p", {
					className: "text-gray-500",
					children: "online"
				})]
			})]
		}), Q.jsxs("div", {
			className: "bg-gray-100 rounded-t-3xl p-4 pb-8 flex flex-col flex-auto",
			children: [Q.jsx(gc, {
				result: n,
				value: e
			}), Q.jsxs("div", {
				className: "flex px-5 py-2 gap-4 flex-none mt-auto rounded-2xl bg-white",
				children: [Q.jsx("input", {
					type: "text",
					className: "p-2 w-full",
					placeholder: "flag",
					value: e,
					onChange: o => t(o.target.value)
				}), Q.jsx("button", {
					className: "w-6",
					onClick: l,
					children: Q.jsx("img", {
						src: Np,
						alt: "send",
						className: "w-full h-full"
					})
				})]
			})]
		})]
	})
}

function Tp() {
	return Q.jsx(Q.Fragment, {
		children: Q.jsx("div", {
			className: "flex justify-center mt-40",
			children: Q.jsx(zp, {})
		})
	})
}
Xl.createRoot(document.getElementById("root")).render(Q.jsx(is.StrictMode, {
	children: Q.jsx(Tp, {})
}));