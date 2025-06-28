import React from 'react';
import UploadForm from './UploadForm';


function App() {
 return (
   <div className="min-h-screen bg-gray-50 p-6">
     <div className="max-w-7xl mx-auto">
       <h1 className="text-4xl font-extrabold text-center text-gray-800 mb-2">
         BudgetAD: FAB Expense Dashboard 📈
       </h1>
       <p className="text-center text-gray-600 mb-6">
         Visualize your NYUAD prepaid card spending and earnings
       </p>
       <UploadForm />
     </div>
   </div>
 );
}


export default App;



