import jwt from "jsonwebtoken";
import User from "../Models/User.js";
import redisClient from "../config/Redis.js";

const authenticateUser = async (req, res, next) => {
  try {
        const refreshToken = req.cookies.refreshToken;
        if (!refreshToken) {
        return res.status(401).json({ message: "No refresh token provided" });
        }

        const isBlacklisted = await redisClient.get(`blacklist_${refreshToken}`);
        if (isBlacklisted) {
        return res.status(401).json({ message: "Token is invalid or logged out" });
        }

        const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);

        const user = await User.findById(decoded.id).select("-password");
        if (!user) {
        return res.status(404).json({ message: "User not found" });
        }

        req.user = user;

        next(); 
    } catch (err) {
        console.error(err);
        return res.status(401).json({ message: "Invalid or expired refresh token" });
    }
};

export default authenticateUser;

