import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from './components/layout/Navbar';
import LoadingSpinner from './components/ui/LoadingSpinner';
import ErrorBoundary from './components/ui/ErrorBoundary';

// Lazy loading للصفحات
const HomePage = React.lazy(() => import('./pages/HomePage'));
const ImageGenerationPage = React.lazy(() => import('./pages/ImageGenerationPage'));
const VideoGenerationPage = React.lazy(() => import('./pages/VideoGenerationPage'));
const AudioGenerationPage = React.lazy(() => import('./pages/AudioGenerationPage'));
const GalleryPage = React.lazy(() => import('./pages/GalleryPage'));
const SettingsPage = React.lazy(() => import('./pages/SettingsPage'));
const AboutPage = React.lazy(() => import('./pages/AboutPage'));

// تأثيرات الانتقال بين الصفحات
const pageVariants = {
  initial: {
    opacity: 0,
    x: 50,
  },
  in: {
    opacity: 1,
    x: 0,
  },
  out: {
    opacity: 0,
    x: -50,
  },
};

const pageTransition = {
  type: 'tween',
  ease: 'anticipate',
  duration: 0.4,
};

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* شريط التنقل */}
        <Navbar />
        
        {/* المحتوى الرئيسي */}
        <main className="pt-16">
          <AnimatePresence mode="wait">
            <Suspense 
              fallback={
                <div className="flex items-center justify-center min-h-screen">
                  <LoadingSpinner size="large" text="جاري تحميل الصفحة..." />
                </div>
              }
            >
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <HomePage />
                    </motion.div>
                  } 
                />
                
                <Route 
                  path="/image-generation" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <ImageGenerationPage />
                    </motion.div>
                  } 
                />
                
                <Route 
                  path="/video-generation" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <VideoGenerationPage />
                    </motion.div>
                  } 
                />
                
                <Route 
                  path="/audio-generation" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <AudioGenerationPage />
                    </motion.div>
                  } 
                />
                
                <Route 
                  path="/gallery" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <GalleryPage />
                    </motion.div>
                  } 
                />
                
                <Route 
                  path="/settings" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <SettingsPage />
                    </motion.div>
                  } 
                />
                
                <Route 
                  path="/about" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <AboutPage />
                    </motion.div>
                  } 
                />
                
                {/* صفحة 404 */}
                <Route 
                  path="*" 
                  element={
                    <motion.div
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                      className="container-custom section-padding"
                    >
                      <div className="text-center">
                        <h1 className="text-6xl font-bold text-gray-900 dark:text-white mb-4">
                          404
                        </h1>
                        <h2 className="text-2xl font-semibold text-gray-700 dark:text-gray-300 mb-6">
                          الصفحة غير موجودة
                        </h2>
                        <p className="text-gray-600 dark:text-gray-400 mb-8">
                          عذراً، الصفحة التي تبحث عنها غير موجودة أو تم نقلها.
                        </p>
                        <motion.a
                          href="/"
                          className="btn-primary inline-block"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          العودة للرئيسية
                        </motion.a>
                      </div>
                    </motion.div>
                  } 
                />
              </Routes>
            </Suspense>
          </AnimatePresence>
        </main>
        
        {/* فوتر */}
        <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
          <div className="container-custom py-8">
            <div className="text-center">
              <p className="text-gray-600 dark:text-gray-400">
                © 2024 SAMIRMAX AI Studio. جميع الحقوق محفوظة.
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                مدعوم بأحدث تقنيات الذكاء الاصطناعي
              </p>
            </div>
          </div>
        </footer>
      </div>
    </ErrorBoundary>
  );
};

export default App;