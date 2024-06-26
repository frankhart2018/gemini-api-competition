import mongoose from "mongoose";

const notificationSchema = mongoose.Schema(
  {
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'users',
        required: true,
      },
      type: {
        type: String,
        required: true,
      },
      redirectionUrl: {
        type: String,
      },
      message: {
        type: String,
        required: true,
      },
      createdAt: {
        type: Date,
        default: Date.now,
      },
  },
  { collection: "notifications" }
);
export default notificationSchema;



