import mongoose from "mongoose";
import userSchema from "./user-schema.js";
const userModel = mongoose.model("UserModel", userSchema);
export default userModel;
