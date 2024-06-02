import questionModel from "./question-model.js";

export const insertQuestions = (questions) => {
    return questionModel.insertMany(questions);
    };

export const getAllQuestions = () => {
    return questionModel.find();
    }