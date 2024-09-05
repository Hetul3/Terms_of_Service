import React, { useState } from 'react';

interface ResponseOutputProps {
    response: any;
}

const ResponseOutput: React.FC<ResponseOutputProps> = React.memo(({ response }) => {
    console.log("response in Response Output", response);
    if(!response) return null;

    return (
        <div className="response-output mt-4 p-4 border border-gray-300 rounded">
          <h2 className="text-lg font-semibold mb-2">API Response:</h2>
          <pre className="text-sm whitespace-pre-wrap bg-gray-100 p-2 rounded">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      );
    });

export default ResponseOutput;