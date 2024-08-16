import React, { useState, FormEvent } from 'react';
import { submitText } from '../api/api';

const TextInput: React.FC = () => {
  const [text, setText] = useState<string>("");
  const [isOpen, setIsOpen] = useState(false);

  const handleSubmitText = (event: FormEvent) => {
    event.preventDefault();
    if (text === null || text.trim() === "") {
      alert("Please enter longer text");
      return;
    }
    submitText(text)
      .then(data => {
        console.log(data);
      })
      .catch(error => console.error(error));
  }

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="w-full mx-auto mt-2 mb-2">
      <button
        onClick={toggleAccordion}
        className="w-full bg-white text-gray-900 py-4 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 ease-in-out transform hover:translate-y-1 focus:outline-none flex items-center"
        style={{
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5 mr-2"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
            clipRule="evenodd"
          />
        </svg>
        Enter Text
      </button>
      
      <div className={`mt-4 overflow-hidden transition-all duration-300 ease-in-out ${isOpen ? 'max-h-96' : 'max-h-0'}`}>
        <form onSubmit={handleSubmitText} className="w-full bg-white rounded-lg shadow-lg p-6">
            <div className="grid gap-2 px-4">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="w-full h-32 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Type your text here..."
              />
            </div>
          <div className="mt-4 flex justify-center">
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 text-white rounded-full shadow hover:bg-indigo-700 focus:outline-none"
            >
              Submit Text
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TextInput;