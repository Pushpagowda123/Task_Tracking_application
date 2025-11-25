import express from "express";
import mongoose from "mongoose";
import { Task } from "../models/task.js";

const router = express.Router();

const serializeTask = (payload) => {
  if (!payload) return null;
  let obj =
    typeof payload.toObject === "function"
      ? payload.toObject({ depopulate: false })
      : { ...payload };

  const assigneeDoc =
    obj.assigneeId && obj.assigneeId._id ? obj.assigneeId : null;

  return {
    ...obj,
    id: obj._id ? obj._id.toString() : obj.id,
    assigneeId: assigneeDoc
      ? assigneeDoc._id.toString()
      : obj.assigneeId
      ? obj.assigneeId?.toString()
      : null,
    assignee: assigneeDoc
      ? {
          id: assigneeDoc._id.toString(),
          name: assigneeDoc.name,
          role: assigneeDoc.role,
        }
      : obj.assignee || null,
    _id: undefined,
    __v: undefined,
  };
};

router.get("/", async (req, res, next) => {
  try {
    const { assigneeId, status } = req.query;
    const query = {};

    if (assigneeId && mongoose.Types.ObjectId.isValid(assigneeId)) {
      query.assigneeId = assigneeId;
    }
    if (status) {
      query.status = status;
    }

    const tasks = await Task.find(query)
      .sort({ createdAt: -1 })
      .populate("assigneeId", "name role");

    res.json(tasks.map(serializeTask));
  } catch (error) {
    next(error);
  }
});

router.post("/", async (req, res, next) => {
  try {
    const assigneeId =
      req.body.assigneeId && mongoose.Types.ObjectId.isValid(req.body.assigneeId)
        ? req.body.assigneeId
        : null;

    const payload = {
      title: req.body.title?.trim(),
      description: req.body.description?.trim() || "",
      priority: req.body.priority || "medium",
      status: req.body.status || "todo",
      assigneeId,
      dueDate: req.body.dueDate ? new Date(req.body.dueDate) : null,
    };

    if (!payload.title) {
      return res.status(400).json({ message: "Title is required." });
    }

    const task = await Task.create(payload);
    const populated = await task.populate("assigneeId", "name role");
    res.status(201).json(serializeTask(populated));
  } catch (error) {
    next(error);
  }
});

router.get("/:id", async (req, res, next) => {
  try {
    const task = await Task.findById(req.params.id).populate("assigneeId", "name role");
    if (!task) {
      return res.status(404).json({ message: "Task not found." });
    }
    res.json(serializeTask(task));
  } catch (error) {
    next(error);
  }
});

router.patch("/:id", async (req, res, next) => {
  try {
    const updates = {};
    const fields = ["title", "description", "priority", "status", "dueDate", "assigneeId"];

    fields.forEach((field) => {
      if (req.body[field] === undefined) return;
      if (field === "dueDate") {
        updates.dueDate = req.body.dueDate ? new Date(req.body.dueDate) : null;
      } else if (field === "assigneeId") {
        updates.assigneeId =
          req.body.assigneeId && mongoose.Types.ObjectId.isValid(req.body.assigneeId)
            ? req.body.assigneeId
            : null;
      } else {
        updates[field] = req.body[field];
      }
    });

    const task = await Task.findByIdAndUpdate(req.params.id, updates, { new: true }).populate(
      "assigneeId",
      "name role"
    );
    if (!task) {
      return res.status(404).json({ message: "Task not found." });
    }
    res.json(serializeTask(task));
  } catch (error) {
    next(error);
  }
});

router.delete("/:id", async (req, res, next) => {
  try {
    const result = await Task.findByIdAndDelete(req.params.id);
    if (!result) {
      return res.status(404).json({ message: "Task not found." });
    }
    res.status(204).send();
  } catch (error) {
    next(error);
  }
});

export default router;

