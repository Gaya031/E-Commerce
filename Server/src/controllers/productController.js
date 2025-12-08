import Product from "../models/Product.js";

const createProduct = async(req, res)=>{
    try{
        const{name, description, price, category, images, stock} = req.body;

        if(!name || !price || !category){
            return res.status(400).json({message: "name, price and catogory are required"});
        }

        const product = await Product.create({
            name,
            description,
            price,
            category,
            images: images || [],
            stock: stock || 0
        });

        return res.status(200).json({
            message: "Product created successfully",
            product
        });
    }catch(err){
        return res.status(500).json({error: err.message});
    }
}

const getAllProduct = async(req,res)=>{
    try{
        const products = await Product.find().sort({createdAt: -1});
        return res.status(200).json({products});
    }catch(err){
        return res.status(500).json({error: err.message});
    }
}

const getProductById = async(req, res)=>{
    try{
        const {productId} = req.params;

        const product = await Product.findById(productId);
        if(!product){
            return res.status(404).json({ message: "Product not found"});
        }
        
        return res.status(200).json({product});
    }catch(err){
        return res.status(500).json({error: err.message});
    }
}

const updateProduct = async (req, res) => {
    try {
        const { productId } = req.params;

        const updated = await Product.findByIdAndUpdate(
            productId,
            req.body,
            { new: true }
        );

        if (!updated) return res.status(404).json({ message: "Product not found" });

        return res.status(200).json({
            message: "Product updated successfully",
            product: updated,
        });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};


const deleteProduct = async(req, res)=>{
    try{
        const {productId} = req.params;

        const deleted = await Product.findByIdAndDelete(productId);

        if(!deleted){
            return res.status(404).json({message: "product not found"});
        }

        return res.status(200).json({message: "product deleted successfully"})
    }catch(err){
        return res.status(500).json({error: err.message})
    }
}

const getProductsByCategory = async (req, res) => {
    try {
        const { category } = req.params;

        const products = await Product.find({ category });

        return res.status(200).json({ products });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};

const searchProducts = async (req, res) => {
    try {
        const { query } = req.query;

        const products = await Product.find({
            name: { $regex: query, $options: "i" },
        });

        return res.status(200).json({ products });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};

const filterProducts = async (req, res) => {
    try {
        const { min, max, rating, category } = req.query;

        let filter = {};

        if (min) filter.price = { ...filter.price, $gte: min };
        if (max) filter.price = { ...filter.price, $lte: max };
        if (rating) filter.rating = { $gte: rating };
        if (category) filter.category = category;

        const products = await Product.find(filter).sort({ price: 1 });

        return res.status(200).json({ products });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};

const getBestSellers = async (req, res) => {
    try {
        const products = await Product.find()
            .sort({ sold: -1 })
            .limit(10);

        return res.status(200).json({ products });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};

const getNewArrivals = async (req, res) => {
    try {
        const products = await Product.find()
            .sort({ createdAt: -1 })
            .limit(10);

        return res.status(200).json({ products });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};


export {
    createProduct, 
    getAllProduct, 
    getProductById, 
    updateProduct, 
    deleteProduct, 
    getProductsByCategory, 
    searchProducts, 
    filterProducts, 
    getBestSellers, 
    getNewArrivals
} 