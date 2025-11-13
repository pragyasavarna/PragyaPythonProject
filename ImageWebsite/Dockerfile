# Use the full Anaconda base image
FROM continuumio/anaconda3

# Set working directory inside container
WORKDIR /app

# Copy environment file first for caching
COPY environment-docker.yml .

# Create conda environment
RUN conda env create -f environment-docker.yml

# Set default shell so conda environment works automatically
SHELL ["conda", "run", "-n", "aiassistant", "/bin/bash", "-c"]

# Copy all project files into container
COPY . .

# ✅ Copy your model into the path expected by views.py
RUN mkdir -p /ImageWebsite/AIModel/Model && \
    cp /app/AIModel/Model/my_model.keras /ImageWebsite/AIModel/Model/ && \
    echo "✅ Model successfully placed at /ImageWebsite/AIModel/Model/my_model.keras"

# ✅ Copy HTML, CSS, JS, and Image folders to absolute paths expected by views.py
RUN mkdir -p /ImageWebsite/HtmlWebsite/CSS \
             /ImageWebsite/HtmlWebsite/Image \
             /ImageWebsite/HtmlWebsite/JavaScript \
             /ImageWebsite/HtmlWebsite/Html && \
    cp -r /app/HtmlWebsite/CSS/* /ImageWebsite/HtmlWebsite/CSS/ || echo "⚠️ No CSS files" && \
    cp -r /app/HtmlWebsite/Image/* /ImageWebsite/HtmlWebsite/Image/ || echo "⚠️ No Image files" && \
    cp -r /app/HtmlWebsite/JavaScript/* /ImageWebsite/HtmlWebsite/JavaScript/ || echo "⚠️ No JS files" && \
    cp -r /app/HtmlWebsite/Html/* /ImageWebsite/HtmlWebsite/Html/ || echo "⚠️ No HTML files"

# ✅ Verify all key paths exist (optional but helpful)
RUN ls -R /ImageWebsite/HtmlWebsite/Html || echo "❌ HTML folder missing!"
RUN ls -R /ImageWebsite/AIModel/Model || echo "❌ Model folder missing!"

# Expose Django default port
EXPOSE 8000

# Run Django server
CMD ["conda", "run", "--no-capture-output", "-n", "aiassistant", "python", "manage.py", "runserver", "0.0.0.0:8000"]
