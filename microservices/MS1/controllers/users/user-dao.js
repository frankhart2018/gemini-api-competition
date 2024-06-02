import userModel from "./user-model.js";

export const findUser = (email) => {
  return userModel.findOne({ email: email });
};


export const createUser = (email, password, username) => {
    return userModel.create({ email, password, username });
    }