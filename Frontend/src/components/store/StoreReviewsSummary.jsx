const BAR_COLORS = {
  5: "bg-green-600",
  4: "bg-lime-500",
  3: "bg-yellow-500",
  2: "bg-orange-500",
  1: "bg-red-500",
};

export default function StoreReviewsSummary({ summary, loading = false, title = "Ratings Summary" }) {
  if (loading) return <p className="text-sm text-gray-600">Loading summary...</p>;
  if (!summary) return null;

  const total = Number(summary.total_reviews || 0);
  const avg = Number(summary.average_rating || 0);
  const breakdown = summary.breakdown || {};

  return (
    <div className="bg-white rounded-xl p-4 border">
      <h4 className="font-semibold mb-3">{title}</h4>
      <div className="flex items-end gap-4 mb-4">
        <div>
          <p className="text-3xl font-bold">{avg.toFixed(1)}</p>
          <p className="text-sm text-gray-500">{total} reviews</p>
        </div>
      </div>
      <div className="space-y-2">
        {[5, 4, 3, 2, 1].map((rating) => {
          const count = Number(breakdown[rating] || 0);
          const pct = total > 0 ? Math.round((count / total) * 100) : 0;
          return (
            <div key={rating} className="flex items-center gap-2 text-sm">
              <span className="w-6">{rating}★</span>
              <div className="h-2 flex-1 bg-gray-100 rounded">
                <div className={`h-2 rounded ${BAR_COLORS[rating]}`} style={{ width: `${pct}%` }} />
              </div>
              <span className="w-16 text-right text-gray-500">{count}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
