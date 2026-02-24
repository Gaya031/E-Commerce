import React from 'react'

const DeliverySchedule = () => {
  const [mode, setMode] = useState("instant");

  return (
    <div className="bg-white p-6 rounded-xl">
      <h2 className="font-semibold mb-4">2. Delivery Schedule</h2>

      <div className="grid grid-cols-2 gap-4">
        <div
          onClick={() => setMode("instant")}
          className={`border p-4 rounded-xl cursor-pointer ${
            mode === "instant"
              ? "border-green-500 bg-green-50"
              : "border-gray-200"
          }`}
        >
          ⚡ <b>Instant Delivery</b>
          <p className="text-sm">Within 30–45 mins</p>
        </div>

        <div
          onClick={() => setMode("scheduled")}
          className={`border p-4 rounded-xl cursor-pointer ${
            mode === "scheduled"
              ? "border-green-500 bg-green-50"
              : "border-gray-200"
          }`}
        >
          🕒 <b>Scheduled</b>
          <p className="text-sm">Choose a time slot</p>
        </div>
      </div>
    </div>
  );
}

export default DeliverySchedule