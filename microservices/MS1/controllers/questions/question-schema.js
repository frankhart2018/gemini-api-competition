import mongoose from "mongoose";

const questionSchema =  mongoose.Schema({
  question_text: { type: String, required: true },
  category: { type: String, required: true },
  created_at: { type: Date, default: Date.now }
},{ collection: "questions" });

export default questionSchema;