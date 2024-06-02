import mongoose from "mongoose";

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