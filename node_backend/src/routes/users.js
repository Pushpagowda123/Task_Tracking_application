import express from "express";
import { User } from "../models/user.js";

const router = express.Router();

router.get("/", async (_req, res, next) => {
  try {
    const users = await User.find().sort({ createdAt: -1 });
    res.json(users);
  } catch (error) {
    next(error);
  }
});

router.post("/", async (req, res, next) => {
  try {
    const name = req.body.name?.trim();
    if (!name) {
      return res.status(400).json({ message: "Name is required." });
    }

    const user = await User.create({
      name,
      role: req.body.role?.trim() || "Contributor",
    });

    res.status(201).json(user);
  } catch (error) {
    next(error);
  }
});

export default router;

