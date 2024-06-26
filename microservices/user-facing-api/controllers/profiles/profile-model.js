import mongoose from "mongoose";
import profileSchema from "./profile-schema.js";
const profileModel = mongoose.model("profileModel", profileSchema);
export default profileModel;
