const crypto = require("crypto");
const fastify = require("fastify")({ logger: true });
const flag = process.env.FLAG ?? "ping{FAKE}";
const secret = crypto.randomUUID() + crypto.randomUUID() + crypto.randomUUID();

const defaultQuotes = {
	flag,
	believing:
		"Believe in yourself... or just gaslight yourself into confidence. Same thing.",
	procrastination:
		"The only way to do great work is to procrastinate until the fear of failure is stronger than your laziness.",
	success:
		"Success is not how high you have climbed, but how well you dodged responsibilities on the way up.",
	crypto:
		"Do what you can, with what you have, where you are... unless it's a crypto investment. Then rethink.",
	shots:
		"You miss 100% of the shots you don't take, but at least you didn't airball on live TV.",
};

const deepCopy = (obj) => JSON.parse(JSON.stringify(obj));

const getAll = (quotes) => {
	const cp = deepCopy(quotes);
	const res = {};
	Object.keys(cp).forEach((k) => {
		if (k === "flag") {
			return;
		}
		res[k] = cp[k];
	});
	return res;
};

fastify.register(require("@fastify/cookie"));
fastify.register(require("@fastify/session"), {
	secret,
	cookieName: "sessionId",
	cookie: { secure: false, httpOnly: true },
	saveUninitialized: false,
	resave: false,
	store: new (require("fastify-session").MemoryStore)(),
});

// Update your own quotes or retrieve
fastify.post("/personalized-quotes", async (req, reply) => {
	const { name, value } = req.body;
	if (!name || typeof name !== "string" || name.length > 50) {
		return reply.status(400).send({ error: "Invalid input" });
	}

	if (!req.session.quotes) {
		req.session.quotes = {};
	}

	if (defaultQuotes[name]) {
		return reply.status(400).send({ error: "Already exists in default" });
	}

	const sanitizedName = name.replace(/[^a-zA-Z0-9 ]/g, "");
	if (value) {
		req.session.quotes[sanitizedName] = value;
		return reply.send({ updated: req.session.quotes[sanitizedName] });
	}
	return reply.send({
		retrieved:
			req.session.quotes[sanitizedName] ?? defaultQuotes[sanitizedName],
	});
});

fastify.get("/personalized-quotes", async (req, reply) => {
	if (!req.session.quotes) {
		req.session.quotes = {};
	}
	return reply.send(req.session.quotes);
});

fastify.get("/default-quotes", async (req, reply) => {
	console.log(req.session.quotes);
	return reply.send(Object.keys(defaultQuotes));
});

fastify.get("/default-quotes/:quoteName", async (req, reply) => {
	const param = req.params["quoteName"];
	if (param === "flag") {
		return reply.status(403).send("not allowed");
	}
	return reply.send(getAll(defaultQuotes)[param] ?? "not found");
});

fastify.listen({ port: 3000, host: "0.0.0.0" }, (err) => {
	if (err) throw err;
	console.log("Server running on http://localhost:3000");
});
