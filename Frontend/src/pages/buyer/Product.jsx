import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { getProduct } from "../../api/product.api";
import { getProductReviewSummary, getProductReviews } from "../../api/review.api";
import { getStoreDetails } from "../../api/store.api";
import ReviewModal from "../../components/store/ReviewModal";
import ReviewsList from "../../components/store/ReviewsList";
import StoreReviewsSummary from "../../components/store/StoreReviewsSummary";
import { useCartStore } from "../../store/cart.store";

const Product = () => {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [store, setStore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [reviews, setReviews] = useState([]);
  const [summary, setSummary] = useState(null);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const addItem = useCartStore((state) => state.addItem);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await getProduct(productId);
        setProduct(res.data);
        
        // Fetch store details
        if (res.data.seller_id) {
          const storeRes = await getStoreDetails(res.data.seller_id);
          setStore(storeRes.data);
        }
        const [reviewsRes, summaryRes] = await Promise.all([
          getProductReviews(productId, { page: 1, size: 20 }),
          getProductReviewSummary(productId),
        ]);
        setReviews(Array.isArray(reviewsRes.data) ? reviewsRes.data : []);
        setSummary(summaryRes.data || null);
      } catch (err) {
        console.error("Error fetching product:", err);
      } finally {
        setLoading(false);
      }
    };

    if (productId) {
      fetchProduct();
    }
  }, [productId]);

  const handleAddToCart = () => {
    addItem(product.seller_id, {
      id: product.id,
      title: product.title,
      price: product.price,
      image: product.images?.[0],
      quantity,
    });
  };

  const refreshReviews = async () => {
    const [reviewsRes, summaryRes] = await Promise.all([
      getProductReviews(productId, { page: 1, size: 20 }),
      getProductReviewSummary(productId),
    ]);
    setReviews(Array.isArray(reviewsRes.data) ? reviewsRes.data : []);
    setSummary(summaryRes.data || null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Product not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Product Image */}
          <div className="bg-white rounded-lg shadow p-4">
            {product.images && product.images.length > 0 ? (
              <img
                src={product.images[0]}
                alt={product.title}
                className="w-full h-96 object-cover rounded-lg"
              />
            ) : (
              <div className="w-full h-96 bg-gray-200 rounded-lg flex items-center justify-center">
                <span className="text-gray-500">No Image</span>
              </div>
            )}
          </div>

          {/* Product Details */}
          <div className="bg-white rounded-lg shadow p-6">
            <h1 className="text-2xl font-bold mb-2">{product.title}</h1>
            
            {store && (
              <p className="text-sm text-gray-600 mb-4">
                Sold by: <span className="font-medium">{store.store_name}</span>
              </p>
            )}
            
            <p className="text-3xl font-bold text-primary mb-4">
              ₹{product.price}
            </p>
            
            {product.stock > 0 ? (
              <p className="text-green-600 mb-4">In Stock ({product.stock} available)</p>
            ) : (
              <p className="text-red-600 mb-4">Out of Stock</p>
            )}

            {/* Quantity Selector */}
            <div className="flex items-center gap-4 mb-6">
              <span className="text-gray-700">Quantity:</span>
              <div className="flex items-center border rounded">
                <button
                  className="px-3 py-1 hover:bg-gray-100"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                >
                  -
                </button>
                <span className="px-3 py-1">{quantity}</span>
                <button
                  className="px-3 py-1 hover:bg-gray-100"
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                >
                  +
                </button>
              </div>
            </div>

            {/* Add to Cart Button */}
            <button
              onClick={handleAddToCart}
              disabled={product.stock <= 0}
              className="w-full bg-primary text-white py-3 rounded-lg font-medium hover:bg-primary/90 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Add to Cart
            </button>

            {/* Product Description */}
            {product.description && (
              <div className="mt-6">
                <h3 className="font-semibold mb-2">Description</h3>
                <p className="text-gray-600">{product.description}</p>
              </div>
            )}

            {/* Category */}
            {product.category && (
              <div className="mt-4">
                <span className="text-sm text-gray-500">Category: {product.category}</span>
              </div>
            )}
            <button
              type="button"
              onClick={() => setShowReviewModal(true)}
              className="mt-6 w-full border border-green-600 text-green-700 rounded-lg py-2 hover:bg-green-50"
            >
              Write a Review
            </button>
          </div>
        </div>

        <div className="mt-8 space-y-4">
          <StoreReviewsSummary summary={summary} title="Product Ratings" />
          <div className="bg-white rounded-xl shadow p-4">
            <h3 className="font-semibold mb-3">Customer Reviews</h3>
            <ReviewsList reviews={reviews} />
          </div>
        </div>
      </div>

      <ReviewModal
        open={showReviewModal}
        onClose={() => setShowReviewModal(false)}
        productId={product?.id}
        onSubmitted={refreshReviews}
      />

      <Footer />
    </div>
  );
};

export default Product;
