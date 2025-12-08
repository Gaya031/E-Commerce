import express from "express"

const productRoute = express.Router();

import { 
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
 } from "../controllers/productController.js";

 productRoute.post('/create', createProduct)
 productRoute.get('/all', getAllProduct)
 
 productRoute.get('/search', searchProducts)

 productRoute.get('/:productId', getProductById)
 productRoute.put('/update/:productId', updateProduct)
 productRoute.delete('/delete/:productId', deleteProduct)

 productRoute.get('/category/:category', getProductsByCategory)
 productRoute.get('/filter', filterProducts)

 productRoute.get('/best-seller', getBestSellers)
 productRoute.get('/new-arrival', getNewArrivals)

 export default productRoute;