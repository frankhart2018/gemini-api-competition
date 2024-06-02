import mongoose from "mongoose";
import questionSchema from "./question-schema.js";
const questionModel = mongoose.model("questionModel", questionSchema);
export default questionModel;
