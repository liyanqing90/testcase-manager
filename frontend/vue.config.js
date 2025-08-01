module.exports = {
  devServer: {
    proxy: {
      '/upload_case': { target: 'http://localhost:5000', changeOrigin: true },
      '/import_case': { target: 'http://localhost:5000', changeOrigin: true }
    }
  }
}; 