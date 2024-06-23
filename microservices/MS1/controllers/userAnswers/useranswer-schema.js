import mongoose from "mongoose";

const UserAnswerSchema = mongoose.Schema({
  user_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionAnsObj: [{
    // question_: {
    //   type: mongoose.Schema.Types.ObjectId,
    //   ref: 'Question',
    //   required: true
    // },
    questionText:{
      type: String,
      required: true
    },
    answer: {
      type: String,
      required: true
    }
  }],
  userSummary:{
    type: String,
  },
  created_at: {
    type: Date,
    default: Date.now
  }
}, { collection: "useranswers" });

export default UserAnswerSchema;