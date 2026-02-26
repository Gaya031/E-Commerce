export default function Footer() {
  return (
    <footer className="bg-white mt-16 border-t">
      <div className="max-w-7xl mx-auto px-4 py-10 grid grid-cols-4 gap-6">
        <div>
          <h4 className="font-bold">RushCart</h4>
          <p className="text-sm text-gray-500 mt-2">
            Fast local delivery from trusted stores.
          </p>
        </div>

        <div>
          <h5 className="font-semibold">Quick Links</h5>
          <p>About</p>
          <p>Careers</p>
        </div>

        <div>
          <h5 className="font-semibold">Categories</h5>
          <p>Vegetables</p>
          <p>Dairy</p>
        </div>

        <div>
          <h5 className="font-semibold">Contact</h5>
          <p>help@rushcart.com</p>
        </div>
      </div>
    </footer>
  );
}
