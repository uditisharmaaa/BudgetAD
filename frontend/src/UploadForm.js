import React, { useState } from 'react';
import axios from 'axios';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [images, setImages] = useState([]);
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState('all');
  const [subscriptions, setSubscriptions] = useState([]);
  const [uploaded, setUploaded] = useState(false);
  const backendURL = 'http://localhost:5002';

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${backendURL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setImages(res.data.images || []);
      setYears(res.data.years || []);
      setSubscriptions(res.data.subscriptions || []);
      setSelectedYear('all');
      setUploaded(true);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed!');
    }
  };

  const filteredImages = images.filter((img) => {
    if (selectedYear === 'all') return true;
    return img.includes(selectedYear);
  });

  const getChartDescription = (imgName) => {
    if (imgName.includes('spending_20')) {
      const year = imgName.match(/spending_(\d{4})/);
      return year
        ? `📅 Monthly Spending - ${year[1]}: Track how your spending changed month by month.`
        : '📅 Monthly Spending';
    }
    if (imgName.includes('top_vendors')) {
      return '🏪 Top 10 Vendors: See which places you spent the most money at.';
    }
    if (imgName.includes('cumulative_balance')) {
      return '📈 Cumulative Balance: See how your card balance changed over time.';
    }
    if (imgName.includes('earnings_vs_spending')) {
      return '💸 Monthly Earnings vs Spending: Compare how much you earned (loaded) vs spent.';
    }
    if (imgName.includes('daily_spending')) {
      return '📊 Daily Spending Trend: Track your day-to-day spending pattern.';
    }
    if (imgName.includes('subscriptions')) {
      return '🔁 Potential Subscriptions: Vendors that charged you on the same date across 3+ months.';
    }
    return '';
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 py-6">

      {/* Instructions */}
      {!uploaded && (
        <div className="space-y-6">
          {/* Blue Info Box about policy change */}
          <div className="bg-blue-100 border border-blue-300 rounded p-4 text-blue-900 shadow text-base">
            <h2 className="font-semibold text-lg mb-2">🔔 Important Update:</h2>
            <p className="leading-relaxed">
              Due to a recent change in FAB's website policy, logins without CAPTCHA are no longer allowed.
              This means automatic scraping is now blocked.
              To use this dashboard, users must now manually download their transaction history as an HTML file and upload it here.
            </p>
          </div>

          {/* Main How-to Block */}
          <div className="bg-blue-50 border border-blue-200 rounded p-4 text-blue-900 shadow text-base">
            <h2 className="text-lg font-semibold mb-2">📥 How to Get Your FAB Card Data</h2>
            <ol className="list-decimal ml-6 space-y-1">
              <li>
                Go to{' '}
                <a
                  href="https://ppc.magnati.com/ppc-inquiry/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-700 underline"
                >
                  https://ppc.magnati.com/ppc-inquiry/
                </a>
              </li>
              <li>Enter your FAB Card details and complete the CAPTCHA manually.</li>
              <li>Once your transactions load, right-click and select <strong>"Save As → Webpage, HTML only"</strong>.</li>
              <li>Upload that saved HTML file here 👇</li>
            </ol>
            <p className="mt-2">Once uploaded, this dashboard will visualize your spending, earnings, top vendors, subscriptions, and more!</p>
          </div>
        </div>
      )}

      {/* Upload Form */}
      <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4 items-center">
        <input type="file" onChange={handleFileChange} className="border p-2 rounded w-full md:w-auto" />
        <button
          type="submit"
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition"
        >
          Upload
        </button>
      </form>

      {/* Year Filter */}
      {years.length > 0 && (
        <div className="flex items-center gap-2">
          <label className="font-medium">Filter by Year:</label>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="border rounded p-2"
          >
            <option value="all">All Years</option>
            {years.map((year, idx) => (
              <option key={idx} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Subscriptions Section */}
      {subscriptions.length > 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded shadow">
          <h2 className="font-bold text-yellow-800 mb-2">🔔 Possible Subscriptions Detected:</h2>
          <ul className="list-disc ml-6 text-yellow-700">
            {subscriptions.map((sub, idx) => (
              <li key={idx}>{sub}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Chart Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        {filteredImages.map((img, idx) => (
          <div key={idx} className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <p className="text-base font-medium text-gray-800 mb-3">{getChartDescription(img)}</p>
            <img
              src={`${backendURL}${img}`}
              alt={`Chart ${idx}`}
              className="w-full h-auto rounded"
              style={{
                maxHeight: '1300px',  // Increase size here
                width: '100%',
                objectFit: 'contain',
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default UploadForm;
