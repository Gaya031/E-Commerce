import mongoose from "mongoose";

const productSchema = new mongoose.Schema({
    name:{
        type: String,
        required: true,
    },
    description:{
        type: String,
        required: true,
    },
    price:{
        type: Number,
        required: true,
    },
    category:{
        // type: mongoose.Schema.Types.ObjectId,
        type: String,
        required: true,
    },
    stock:{
        type: Number,
        required: true,
        default: 0,
    },
    images:[
        {
            url: String,
            public_id: String,
        },
    ],
    ratings:{
        type: Number,
        default: 0,
    },
    totalReviews:{
        type: Number,
        default: 0,
    },
  },
  { timestamps: true }
);

const Product = mongoose.model('Product', productSchema);
export default Product;
