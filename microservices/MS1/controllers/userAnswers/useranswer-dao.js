import userAnswerModel from "./useranswer-model.js";

export const findUser = (userId) => {
    return userAnswerModel.findOne({ user_id: userId });
    };

export const createOrUpdateUserAnswer = (userId, questionAnsObj) => {
    return userAnswerModel.findOneAndUpdate(
        { user_id: userId }, 
        { $set: { questionAnsObj } }, 
        { new: true, upsert: true }
    );
}