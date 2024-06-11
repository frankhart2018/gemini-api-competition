import * as userDao from "./user-dao.js";
import bcrypt from "bcryptjs";
import Jwt from "jsonwebtoken";
import nodemailer from "nodemailer";
import dotenv from 'dotenv';
dotenv.config();
const JWT_SECRET = process.env.JWT_SECRET;
const PROJECT_URL = process.env.PROJECT_URL||"http://localhost:4000";
const UsersController = (app) => {
    app.post("/api/login", findUser);
    app.post("/api/register", createUser);
    app.post("/api/logout", logoutUser);
    app.post("/api/forget-password", forgetPassword);
    app.post("/api/update-password/:id/:token", updatePassword);
}

const findUser = async (req, res) => {
    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).send({ message: "Email and password are required" });
        }
        const user = await userDao.findUser(email);
        if (!user) {
            return res.status(404).send({ message: "User not found" });
        }
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).send({ message: "Invalid credentials" });
        }
        const token = Jwt.sign({ id: user._id }, JWT_SECRET, { expiresIn: "1h" });
        res.send({ userId:user._id, token });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}


const createUser = async (req, res) => {
    try {
        const { email, password, username } = req.body;

        // Validate inputs
        if (!email || !password || !username) {
            return res.status(400).json({ message: "Email, password, and username are required" });
        }

        const userPresent = await userDao.findUser(email);
        if (userPresent) {
            return res.status(400).json({ message: "User already exists" });
        }
        const usernameExists = await userDao.findUserByUsername(username);
        if (usernameExists) {
            return res.status(400).json({ message: "Username already exists" });
        }

        const encryptedPassword = await bcrypt.hash(password, 10);
        await userDao.createUser(email, encryptedPassword, username);

        const token = Jwt.sign({ email: email }, JWT_SECRET, { expiresIn: 86400 });
        res.status(201).json({
            message: "User created successfully",
            status: "ok",
            data: token,
            userId:user._id
        });
    } catch (error) {
        res.status(500).json({ message: "An error occurred" });
    }
};

   
const logoutUser = async (req, res) => {
    try {
        // JWT is stateless, so we don't need to do anything here to log out. Client will delete the token.
        const { email } = req.body;
        if (!email) {
            return res.status(400).send({ message: "Email is required" });
        }
        res.send({ message: "User logged out" });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

const forgetPassword = async (req, res) => {
    const { email } = req.body;
    const user = await userDao.findUser(email);
    if (!user) {
      return res.json({ status: "404", message: "User Not found" });
    }
    const secret = JWT_SECRET + user.password;
    const token = Jwt.sign({ email: user.email, id: user._id }, secret, {
      expiresIn: "5m",
    });
    const link = `${PROJECT_URL}/api/update-password/${user._id}/${token}`;
    var transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: "team27neu@gmail.com",
        pass: "gvsvokpuxkhwsezu",
      },
    });
  
    var mailOptions = {
      from: "team27neu@gmail.com",
      to: user.email,
      subject: "Password Reset",
      text: link,
    };
  
    transporter.sendMail(mailOptions, function (error, info) {
      if (error) {
      } else {
        console.log("Email sent: " + info.response);
      }
    });
    res.status(201).json({ status: "ok", message: "Email sent" });
  };




const updatePassword = async (req, res) => {
    const { id, token } = req.params;
    const { password } = req.body;
    const oldUser = await userDao.findUserById({ _id: id });
    if (!oldUser) {
      return res.json({ status: 400, message: "User Not Exists!!" });
    }
    const secret = JWT_SECRET + oldUser.password;
    try {
      Jwt.verify(token, secret);
      const encryptedPassword = await bcrypt.hash(password, 10);
      await userDao.updatePassword(id, encryptedPassword);
      return res.status(201).json({
        status: 201,
        message: "Password Updated Successfully",
      });
    } catch (error) {
      return res.status(400).json({ status: 400, message: "Invalid Token" });
    }
  };
  
export default UsersController;
