import mongoose from "mongoose";
import userAnswerSchema from "./useranswer-schema.js";
const userAnswerModel = mongoose.model("userAnswerModel", userAnswerSchema);
export default userAnswerModel;
