import mongoose from "mongoose";

const UserAnswerSchema = mongoose.Schema({
  user_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionAnsObj: [{
   
    questionText:{
      type: String,
      required: true
    },
    answer: {
      type: String,
      required: true
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    status:{type:String,enum:['pending','accepted','declined'],default:'pending'}
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