import React, { useState } from 'react';
import { submitFeedback } from '../api/api';
import { CheckCircle, XCircle } from 'lucide-react';

interface ResponseOutputProps {
  response: any;
}

interface FeedbackState {
  [key: string]: {
    submitted: boolean;
    type: 'Positive' | 'Negative' | null;
  };
}

const ResponseOutput: React.FC<ResponseOutputProps> = React.memo(({ response }) => {
  const [activeTooltip, setActiveTooltip] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [feedbackState, setFeedbackState] = useState<FeedbackState>({});

  if (!response) return null;

  const colors: string[] = [
    'bg-blue-100',
    'bg-green-100',
    'bg-yellow-100',
    'bg-pink-100',
    'bg-purple-100'
  ];

  const severityColors: Record<string, string> = {
    'First Party Collection/Use': 'bg-red-100',
    'Third Party Sharing/Collection': 'bg-red-100',
    'User Access, Edit and Deletion': 'bg-orange-100',
    'Data Retention': 'bg-yellow-100',
    'Data Security': 'bg-yellow-100',
    'International and Specific Audiences': 'bg-white',
    'Do Not Track': 'bg-white',
    'Policy Change': 'bg-yellow-100',
    'User Choice/Control': 'bg-white',
    'Introductory/Generic': 'bg-green-100',
    'Practice not covered': 'bg-yellow-100',
    'Privacy contact information': 'bg-yellow-100',
  };

  const handleFeedback = async (feedbackType: boolean, classification: string, explanation: string, phrase: string) => {
    setIsSubmitting(true);
    try {
      await submitFeedback(feedbackType, classification, explanation, phrase);
      setFeedbackState(prev => ({
        ...prev,
        [phrase]: {
          submitted: true,
          type: feedbackType ? 'Positive' : 'Negative'
        }
      }));
    } catch (error) {
      console.error('Error submitting feedback:', error);
      // You might want to add some error handling UI here
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="response-output mb-4 mt-4 p-4 border rounded bg-white shadow-md rounded-xl">
      <h2 className="text-lg font-semibold mb-2">Response Analysis</h2>
      <div className="leading-relaxed">
        {response.order.map((phrase: string, index: number) => {
          const classification = response.response[phrase]?.classification;
          const explanation = response.response[phrase]?.explanation;
          const tooltipColor = severityColors[classification] || 'bg-gray-100';
          const feedbackSubmitted = feedbackState[phrase]?.submitted;
          const feedbackType = feedbackState[phrase]?.type;

          return (
            <span
              key={index}
              className="relative inline"
              onMouseEnter={() => setActiveTooltip(phrase)}
              onMouseLeave={() => setActiveTooltip(null)}
            >
              <span className={`px-1 py-0.5 text-lg rounded cursor-pointer transition-colors duration-200 ${colors[index % colors.length]}`}>
                {phrase}
              </span>
              {activeTooltip === phrase && (
                <div className={`absolute z-10 w-72 p-2 mb-2 text-md border border-gray-200 rounded-md shadow-lg bottom-full left-1/2 transform -translate-x-1/2 ${tooltipColor}`}>
                  <div className="font-semibold mb-1">
                    {classification}
                  </div>
                  <div className="text-gray-600 mb-2">
                    {explanation}
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="font-medium">
                      {feedbackSubmitted 
                        ? `Feedback: ${feedbackType}` 
                        : 'Feedback:'}
                    </span>
                    {!feedbackSubmitted && (
                      <div className="space-x-2">
                        <button
                          onClick={() => handleFeedback(true, classification, explanation, phrase)}
                          disabled={isSubmitting}
                          className="text-green-500 hover:text-green-600 disabled:opacity-50"
                        >
                          <CheckCircle size={24} />
                        </button>
                        <button
                          onClick={() => handleFeedback(false, classification, explanation, phrase)}
                          disabled={isSubmitting}
                          className="text-red-500 hover:text-red-600 disabled:opacity-50"
                        >
                          <XCircle size={24} />
                        </button>
                      </div>
                    )}
                  </div>
                  <div className={`absolute w-3 h-3 border-b border-r border-gray-200 transform rotate-45 -bottom-1.5 left-1/2 -ml-1.5 ${tooltipColor}`}></div>
                </div>
              )}
              {' '}
            </span>
          );
        })}
      </div>
    </div>
  );
});

export default ResponseOutput;