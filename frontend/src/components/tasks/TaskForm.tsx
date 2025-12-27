/**
 * TaskForm component.
 * Handles task creation with Phase 5 features: priorities, tags, due dates, reminders, recurrence.
 */
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { tasksApi, ApiError, Task } from "@/lib/api";
import { toast } from "sonner";
import { Plus, X, Calendar, Bell, RotateCcw } from "lucide-react";

interface TaskFormProps {
  onTaskCreated?: (task: Task) => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [remindAt, setRemindAt] = useState("");
  const [recurrence, setRecurrence] = useState("none");
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{
    title?: string;
    description?: string;
    dueDate?: string;
    remindAt?: string;
    tags?: string;
    general?: string;
  }>({});

  const validateForm = (): boolean => {
    const newErrors: typeof errors = {};

    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.length > 200) {
      newErrors.title = "Title must be 200 characters or less";
    }

    if (description.length > 2000) {
      newErrors.description = "Description must be 2000 characters or less";
    }

    // Validate due date format if provided
    if (dueDate && isNaN(Date.parse(dueDate))) {
      newErrors.dueDate = "Invalid date format";
    }

    // Validate remind_at format if provided
    if (remindAt && isNaN(Date.parse(remindAt))) {
      newErrors.remindAt = "Invalid date format";
    }

    // Validate tags
    if (tags.length > 10) {
      newErrors.tags = "Maximum 10 tags allowed";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const addTag = () => {
    const tag = tagInput.trim().toLowerCase();
    if (tag && !tags.includes(tag) && tags.length < 10) {
      setTags([...tags, tag]);
      setTagInput("");
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleTagKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addTag();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      const task = await tasksApi.create({
        title: title.trim(),
        description: description.trim() || undefined,
        priority: priority as "low" | "medium" | "high",
        due_date: dueDate || undefined,
        remind_at: remindAt || undefined,
        recurrence: recurrence as "none" | "daily" | "weekly" | "monthly",
        tags: tags.length > 0 ? tags : undefined,
      });

      toast.success("Task created successfully!");

      // Reset form
      setTitle("");
      setDescription("");
      setPriority("medium");
      setDueDate("");
      setRemindAt("");
      setRecurrence("none");
      setTags([]);
      setTagInput("");

      // Notify parent component
      if (onTaskCreated) {
        onTaskCreated(task);
      }
    } catch (error) {
      if (error instanceof ApiError) {
        const detail = error.data?.detail || "Failed to create task";
        setErrors({ general: detail });
        toast.error(detail);
      } else {
        setErrors({ general: "An unexpected error occurred" });
        toast.error("An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="sticky top-4">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-lg">
          <Plus className="h-5 w-5 text-primary" />
          Create New Task
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title" className="text-sm font-medium">
              Title <span className="text-destructive">*</span>
            </Label>
            <Input
              id="title"
              placeholder="Enter task title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isLoading}
              aria-invalid={!!errors.title}
              maxLength={200}
            />
            {errors.title && (
              <p className="text-sm text-destructive">{errors.title}</p>
            )}
            <p className="text-xs text-muted-foreground">
              {title.length}/200 characters
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description" className="text-sm font-medium">Description</Label>
            <textarea
              id="description"
              placeholder="Enter task description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isLoading}
              aria-invalid={!!errors.description}
              maxLength={2000}
              rows={4}
              className="flex w-full rounded-lg border border-input bg-background px-4 py-3 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:border-transparent disabled:cursor-not-allowed disabled:opacity-50 resize-none"
            />
            {errors.description && (
              <p className="text-sm text-destructive">{errors.description}</p>
            )}
            <p className="text-xs text-muted-foreground">
              {description.length}/2000 characters
            </p>
          </div>

          {/* Priority */}
          <div className="space-y-2">
            <Label htmlFor="priority" className="text-sm font-medium">Priority</Label>
            <Select value={priority} onValueChange={setPriority} disabled={isLoading}>
              <SelectTrigger>
                <SelectValue placeholder="Select priority" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="low">Low</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="high">High</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Due Date */}
          <div className="space-y-2">
            <Label htmlFor="dueDate" className="text-sm font-medium flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Due Date
            </Label>
            <Input
              id="dueDate"
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              disabled={isLoading}
              aria-invalid={!!errors.dueDate}
            />
            {errors.dueDate && (
              <p className="text-sm text-destructive">{errors.dueDate}</p>
            )}
          </div>

          {/* Reminder */}
          <div className="space-y-2">
            <Label htmlFor="remindAt" className="text-sm font-medium flex items-center gap-2">
              <Bell className="h-4 w-4" />
              Reminder
            </Label>
            <Input
              id="remindAt"
              type="datetime-local"
              value={remindAt}
              onChange={(e) => setRemindAt(e.target.value)}
              disabled={isLoading}
              aria-invalid={!!errors.remindAt}
            />
            {errors.remindAt && (
              <p className="text-sm text-destructive">{errors.remindAt}</p>
            )}
          </div>

          {/* Recurrence */}
          <div className="space-y-2">
            <Label htmlFor="recurrence" className="text-sm font-medium flex items-center gap-2">
              <RotateCcw className="h-4 w-4" />
              Recurrence
            </Label>
            <Select value={recurrence} onValueChange={setRecurrence} disabled={isLoading}>
              <SelectTrigger>
                <SelectValue placeholder="Select recurrence" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">None</SelectItem>
                <SelectItem value="daily">Daily</SelectItem>
                <SelectItem value="weekly">Weekly</SelectItem>
                <SelectItem value="monthly">Monthly</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Tags */}
          <div className="space-y-2">
            <Label htmlFor="tags" className="text-sm font-medium">Tags</Label>
            <div className="flex gap-2">
              <Input
                id="tagInput"
                placeholder="Add a tag"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={handleTagKeyPress}
                disabled={isLoading || tags.length >= 10}
                maxLength={50}
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addTag}
                disabled={isLoading || !tagInput.trim() || tags.length >= 10}
              >
                Add
              </Button>
            </div>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {tags.map((tag) => (
                  <Badge key={tag} variant="secondary" className="flex items-center gap-1">
                    {tag}
                    <button
                      type="button"
                      onClick={() => removeTag(tag)}
                      disabled={isLoading}
                      className="ml-1 hover:text-destructive"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            )}
            {errors.tags && (
              <p className="text-sm text-destructive">{errors.tags}</p>
            )}
            <p className="text-xs text-muted-foreground">
              {tags.length}/10 tags
            </p>
          </div>

          {errors.general && (
            <div className="p-4 text-sm text-destructive bg-destructive/10 rounded-lg border border-destructive/20">
              {errors.general}
            </div>
          )}

          <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
            {isLoading ? (
              "Creating..."
            ) : (
              <>
                <Plus className="h-4 w-4" />
                Create Task
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
