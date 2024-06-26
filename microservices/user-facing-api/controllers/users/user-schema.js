import mongoose from "mongoose";

const userSchema = mongoose.Schema(
  {
    username: {
        type: String,
        required: true,
        unique: true,
      },
      email: {
        type: String,
        required: true,
        unique: true,
      },
      password: {
        type: String,
      },
      createdAt: {
        type: Date,
        default: Date.now,
      },
  },
  { collection: "users" }
);
export default userSchema;



