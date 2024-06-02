import profileModel from "./profile-model.js";
export const findProfile = (userId) => {
  return profileModel.findOne({ userId: userId });
}

export const createProfile = (userId, bio, age, location, interests) => {
  return profileModel.create({ userId, bio, age, location, interests });
}

export const updateProfile = (userId, bio, age, location, interests) => {
  return profileModel.findOneAndUpdate({ userId: userId }, { bio, age, location, interests }, { new: true });
}