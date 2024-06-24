import mongoose from "mongoose";

const FriendSchema = mongoose.Schema({
    receiverId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    status: { type: String, enum: ['pending', 'accepted', 'declined'], required: true }
  });

const ProfileSchema = mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'users',
    required: true,
  },
  bio: {
    type: String,
    maxlength: 500,
  },
  age:{
    type: Number,
  },
  friends: [FriendSchema],
//   profilePicture: {
//     type: String,
//   },
//   coverPhoto: {
//     type: String,
//   },
//   education: [
//     {
//       school: String,
//       degree: String,
//       fieldOfStudy: String,
//       startDate: Date,
//       endDate: Date,
//       description: String,
//     }
//   ],
//   work: [
//     {
//       company: String,
//       position: String,
//       startDate: Date,
//       endDate: Date,
//       description: String,
//     }
//   ],
  location: {
    city: String,
    country: String,
  },
//   friends: [
//     {
//       type: mongoose.Schema.Types.ObjectId,
//       ref: 'userModel',
//     }
//   ],
  interests: [String],
//   posts: [
//     {
//       type: mongoose.Schema.Types.ObjectId,
//       ref: 'Post',
//     }
//   ],
  createdAt: {
    type: Date,
    default: Date.now,
  },
//   updatedAt: {
//     type: Date,
//     default: Date.now,
//   }
}, { collection: "profiles" }
);
export default ProfileSchema;