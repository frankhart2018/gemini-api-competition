import { connect } from 'mongoose';

const connectDB = async () => {
  try {
    await connect(process.env.DB_CONNECTION_STRING || "mongodb://localhost:27017/MS1", {
    });
    
    console.log('MongoDB connected');
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
};

export default connectDB;