import * as userAnswerDao from "./useranswer-dao.js";
import * as userDao from "../users/user-dao.js";
import {logger, LogLevel} from "../../utils/logging.js";
import dotenv from 'dotenv';
const UserAnswerController = (app) => {
    app.post("/api/questions/answers", createUpdateUserAnswer);
    app.get("/api/useranswers/:userId", getUserAnswers);
}
dotenv.config();
const PROMPT_URL = process.env.PROMPT_URL;
const createUpdateUserAnswer = async (req, res) => {
    try {
        const { userId, questionAnsObj} = req.body;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        if (!Array.isArray(questionAnsObj) || !questionAnsObj.every(obj => obj.hasOwnProperty('questionText') && obj.hasOwnProperty('answer'))) {
            return res.status(400).send({ message: "questionAnsObj must be an array of objects with questionText and answer properties" });
        }
        //insert user_id or update if already exists
        const userPresent = await userDao.findUserById(userId);
        if(!userPresent){
           // user not present return 404
           return res.status(404).send({ message: "User not found" });
        }
        const prompt = generatePrompt(questionAnsObj);
        const summary = await generateSummary(prompt);

        await userAnswerDao.createOrUpdateUserAnswer(userId, questionAnsObj,summary);
        res.send({ message: "User info added successfully" });
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
}
const getUserAnswers = async (req, res) => {
    try {
        const userId = req.params.userId;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        const user = await userDao.findUserById(userId);
        if (!user) {
            return res.status(404).send({ message: "User not found" });
        }
        res.send(user);
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
}

const generatePrompt = (questionAnsObj) => {
    const qaString = questionAnsObj.map(qa => `Q: ${qa.questionText} A: ${qa.answer}`).join('\n');
    const prompt = `You are an extremely knowledgeable person who will use the text with Question_text marked as Q and answers marked as A. Use this information to generate a user summary. Only use the user-provided information, don't make any fake stories. Think like a human.\n\n${qaString}`;
    return prompt;
}
const generateSummary = async (prompt) => {
    const response = await fetch(`${PROMPT_URL}/gemini-agents/prompt`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt, poll: true })
    });

    if (!response.ok) {
        throw new Error(`Error generating summary: ${response.statusText}`);
    }

    const data = await response.json();
    return data.output;
}

export default UserAnswerController;