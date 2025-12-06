const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());

const MONGO_URI = process.env.MONGO_URI;

mongoose.connect(MONGO_URI)
  .then(() => console.log("✅ MongoDB Connected"))
  .catch(err => console.error("❌ MongoDB Error:", err));

// Schema
const Memory = mongoose.model("Memory", {
  location: String,
  date: String,
  description: String,
  imageUrl: String
});

// ✅ Create Memory
app.post("/memories", async (req, res) => {
  try {
    const memory = new Memory(req.body);
    await memory.save();
    res.status(201).send(memory);
  } catch (err) {
    res.status(400).send({ error: "Error creating memory" });
  }
});

// ✅ Get All Memories
app.get("/memories", async (req, res) => {
  const memories = await Memory.find();
  res.send(memories);
});

// ✅ Get Single Memory
app.get("/memories/:id", async (req, res) => {
  const memory = await Memory.findById(req.params.id);
  memory ? res.send(memory) : res.status(404).send({ error: "Not found" });
});

// ✅ Update Memory
app.put("/memories/:id", async (req, res) => {
  const memory = await Memory.findByIdAndUpdate(req.params.id, req.body, { new: true });
  memory ? res.send(memory) : res.status(404).send({ error: "Not found" });
});

// ✅ Delete Memory
app.delete("/memories/:id", async (req, res) => {
  await Memory.findByIdAndDelete(req.params.id);
  res.send({ message: "Deleted successfully" });
});

// ✅ Health Check
app.get("/health", (req, res) => res.send("OK"));

app.listen(3000, () => console.log("🚀 Server running on port 3000"));
