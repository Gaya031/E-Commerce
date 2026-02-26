export default function ReviewsList({ reviews = [], loading = false, emptyText = "No reviews yet." }) {
  if (loading) return <p className="text-sm text-gray-600">Loading reviews...</p>;
  if (!reviews.length) return <p className="text-sm text-gray-600">{emptyText}</p>;

  return (
    <div className="space-y-3">
      {reviews.map((review) => (
        <div key={review.id} className="border rounded-lg p-3">
          <div className="flex items-center justify-between">
            <p className="font-medium text-sm">Rating: {review.rating}/5</p>
            {review.created_at && (
              <p className="text-xs text-gray-500">{new Date(review.created_at).toLocaleDateString()}</p>
            )}
          </div>
          <p className="text-sm text-gray-700 mt-1">{review.comment || "No comment provided."}</p>
        </div>
      ))}
    </div>
  );
}
