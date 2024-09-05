import React, { useState, useEffect, FormEvent } from 'react';
import ImageInput from '../components/ImageInput';
import TextInput from '../components/TextInput';
import UrlInput from '../components/UrlInput';
import ResponseOutput from '../components/ResponseOutput';
import {submitUrl, submitText} from '../api/api';

const Home: React.FC = () => {
  const [headerVisible1, setHeaderVisible1] = useState<boolean>(false);
  const [headerVisible2, setHeaderVisible2] = useState<boolean>(false);
  const [description, setDescription] = useState<string>("");
  const [output, setOutput] = useState<any>(null);
  const fullDescription = "Select how you want to paste your terms and conditions. Our advanced AI-powered system will analyze the document for potential issues and inconsistencies!";

  const handleSubmitText = (event: FormEvent, text: string) => {
    event.preventDefault();
    if (text === null || text.trim() === "") {
      alert("Please enter longer text");
      return;
    }
    submitText(text)
      .then(data => {
        console.log(data);
        setOutput(data);
      })
      .catch(error => console.error(error));
  }

  const handleUrlSubmit = (event: FormEvent, url: string) => {
    event.preventDefault();
    const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
    if (!urlRegex.test(url)) {
      alert("Please enter a valid URL");
      return;
    }
    submitUrl(url)
      .then(data => {
        console.log(data);
        setOutput(data);
      })
      .catch(error => console.error(error));
  }

  useEffect(() => {
    const headerTimeout1 = setTimeout(() => setHeaderVisible1(true), 500);
    const headerTimeout2 = setTimeout(() => setHeaderVisible2(true), 1500);
  
    let charIndex = 0;
    const typingTimeout = setTimeout(() => {
      const typingInterval = setInterval(() => {
        if (charIndex < fullDescription.length) {
          setDescription(fullDescription.slice(0, charIndex + 1));
          charIndex++;
        } else {
          clearInterval(typingInterval);
        }
      }, 25);
      return () => clearInterval(typingInterval);
    }, 2000); 
  
    return () => {
      clearTimeout(headerTimeout1);
      clearTimeout(headerTimeout2);
      clearTimeout(typingTimeout);
    };
  }, []);

  return (
    <div className="min-h-screen bg-bone flex flex-col items-center justify-center font-sans">
      <div className="w-3/4 max-w-3xl">
        <h1 className="text-6xl font-bold mb-4">
          <span className={`block transition-all duration-2000 ease-out ${
            headerVisible1 ? "transform translate-y-0 opacity-100" : "transform -translate-y-20 opacity-0"
          }`}>
            Your Terms and
          </span>
          <span className={`block transition-all duration-2000 ease-out ${
            headerVisible2 ? "transform translate-y-0 opacity-100" : "transform -translate-y-5 opacity-0"
          }`}>
            Conditions Checker!
          </span>
        </h1>
        <div className="mt-4 text-xl text-gray-700" style={{ height: '75px', overflow: 'hidden' }}>
          <p>{description}</p>
        </div>
        <div className="mt-8">
          <TextInput onSubmit={handleSubmitText}/>
          <UrlInput onSubmit={handleUrlSubmit}/>
          <ImageInput />
          <ResponseOutput response={output}/>
        </div>
      </div>
    </div>
  );
}

export default Home;