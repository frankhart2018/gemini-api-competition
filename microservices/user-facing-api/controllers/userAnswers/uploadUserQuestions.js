import * as userAnswerDao from "./useranswer-dao.js";
import * as userDao from "../users/user-dao.js";
import { logger, LogLevel } from "../../utils/logging.js";
import { MinioClient } from "../../utils/minio.js";
import fs from 'fs/promises';
import dotenv from 'dotenv';
dotenv.config();

const minioClient = new MinioClient();

const uploadUserQuestions = async (req, res) => {
    try {
        const userId = req.params.userId;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        const user = await userDao.findUserById(userId);
        if (!user) {
            return res.status(404).send({ message: "User not found" });
        }
        let questionAnsObj = [];
        let newQuestionAnsObj = [];

        //called from microservice to upload new questions
        if(req.body.questionAnsObj.length>0){
            newQuestionAnsObj = req.body.questionAnsObj;
        } else {
        const localFilePath = "../../static/questions.json";

        await minioClient.downloadFile("questions", "questions.json", localFilePath);

        // Read the file using fs.promises
        const fileData = await fs.readFile(localFilePath, 'utf-8');

        // Parse the JSON data
        const questions = JSON.parse(fileData);
        questionAnsObj = questions.map(q => ({
            questionText: q.question_text,
            answer: '',
            isRequired: q.category === 'Required',
            status: 'pending'
        }));
        await userAnswerDao.createOrUpdateUserAnswer(userId, questionAnsObj, '');
        return ;
    }
    if (newQuestionAnsObj && newQuestionAnsObj.length > 0) {
        // If so, append them to the existing `questionAnsObj`
        const userAnswers = await userAnswerDao.findUser(userId);
        questionAnsObj = userAnswers.questionAnsObj;
        questionAnsObj = [...questionAnsObj, ...newQuestionAnsObj];
        await userAnswerDao.createOrUpdateUserAnswer(userId, questionAnsObj, '');
        res.send({ message: "Questions uploaded successfully" });
    }
       
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
};

export default uploadUserQuestions;
