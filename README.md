# Final Project: Solving the Dropout Issue at Jaya Jaya Institute

## Business Understanding

> Jaya Jaya Institute is a higher education institution established in 2000, known for producing high-quality graduates. However, the high rate of student dropouts has become a serious concern. Dropouts not only impact the institution's reputation but also cause financial losses and the loss of potential contributions from students. To reduce the dropout rate, Jaya Jaya Institute aims to implement an early prediction system that can identify high-risk students from the beginning of their academic journey.

### Business Problems

1. How can we identify students at risk of dropping out early in their studies?
2. What are the key factors that influence a student's likelihood of dropping out?
3. How can student performance visualizations support institutional decision-making?

### Project Scope

- Perform data exploration and visualization to understand the distribution and relationships between features.
- Build a classification model to predict whether a student is likely to drop out.
- Develop a visual dashboard to monitor student performance.
- Provide a predictive system prototype that can be directly accessed via Streamlit.

### Preparation

**Data source**: The Student dataset contains academic information, student background, student status, and more. It is stored in the file [**students-performance.csv**](students-performance.csv), or you can download it directly from [dicoding_dataset](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance).

**Environment setup**:

## ⚙️Installation
Make sure all required dependencies are installed:
```
pip install -r requirements.txt
```
---

## 🎞️Running the Project
1️⃣ Launch the Jupyter Notebook or open it in Google Colab:
   ```
   jupyter notebook Proyek_Droupout_Prediction.ipynb
   ```

2️⃣ Follow the steps in the notebook to train and evaluate the LightGBM model.

3️⃣ Save the trained LightGBM model, or **if you wish to skip the training process in step 2**, you can directly download the following files:  
[LightGBM_model.pkl](LightGBM_model.pkl), [pipeline.pkl](pipeline_lightgbm.pkl), [optimal_threshold.json](optimal_threshold.json), [features_train.json](expected_columns.json), and [top_feature_importance.csv](feature_importance.csv).

- `LightGBM_model.pkl`: Contains the trained LightGBM model used to predict students at risk of dropping out.  
- `pipeline.pkl`: Contains the preprocessing pipeline (e.g., encoding and scaling) required before the model can make predictions.  
- `optimal_threshold.json`: Stores the optimal threshold value (**0.58**) used to convert predicted probabilities into final classes (dropout `1` or not `0`).  
- `top_feature_importance.csv`: Lists the most influential features in dropout prediction, useful for understanding the key contributing factors.  
- `features_train.json`: A JSON file containing the list of feature names used during model training. **This file serves to:**

  1. **Validate Input**: Ensure any newly uploaded dataset has exactly the same column names as the training data.  
  2. **Maintain Consistency**: Preserve the order and presence of features before they are passed through the preprocessing pipeline, ensuring transformations and predictions run without errors.

These files are required to run [app.py](app.py) without retraining the model.

4️⃣ Next, run the [app.py](app.py) file to launch the student dropout prediction prototype using Streamlit.  
Alternatively, if you prefer to skip this step, you can directly access the deployed prototype via Streamlit here:  
👉 [Streamlit App](https://proyekstudentdropoutpredicition-rifky2xe7kdqtykfxbcgcw.streamlit.app/)

Below is an explanation of the main processes inside `app.py`:

### **📄 Process Overview in app.py:**
```
1. Import Libraries  
- Import all necessary libraries for data processing, model loading, and prediction.

2. Load Model and Related Files  
- `pipeline.pkl`: Used for data preprocessing (such as encoding and scaling).  
- `LightGBM_model.pkl`: The trained LightGBM model used to predict whether a student is likely to drop out.  
- `optimal_threshold.json`: Contains the optimal threshold value (0.58) used to convert prediction probabilities into binary class labels (0 = not dropout, 1 = dropout).  
- `expected_columns.json`: A list of feature (column) names used during model training.

3. Load Student Data  
- Reads the `students_performance.csv` file containing student data to be predicted.

4. Data Preprocessing  
- Student data is processed using the same pipeline that was applied during model training.

5. Prediction  
- The model outputs the probability of a student potentially dropping out.  
- These probabilities are then converted into binary labels based on the threshold value (0.58).

6. Prediction Results  
- New columns are added to the DataFrame:  
  - `Predicted_Dropout`: The prediction result indicating whether the student is likely to drop out.  
  - `Dropout_Probability`: The predicted probability of the student potentially dropping out.

7. Save Results  
- The final results are saved to a file named `probability_export.csv`.
```

## 🎯Business Dashboard

**The dashboard is organized sequentially to provide a clear narrative:**

1. **Total Number of Students**: Displays a total of 4,424 student records.
2. **Dropout Predictions**: Shows the number of students predicted to drop out (1,388 or ~31.4%).
3. **Top 10 Factors Influencing Student Dropout**: The most influential features include `Admission_grade`, `Previous_qualification_grade`, `Course`, and `Mothers_occupation`.
4. **Retention Strategy**: Developed based on insights derived from the most important features.

## ✨Running the Metabase Dashboard via Docker

1️⃣ **Convert Files to SQLite Database**

Before being used in **Metabase**, the prediction results file **[probability_export.csv](probability_export.csv)** and the feature importance file **[top_feature_importance.csv](feature_importance.csv)** must be converted into a **SQLite (.db)** database.

To perform the conversion, you can either run the code provided in [convert.py](convert.py),  
or directly download the converted SQLite database here: [Predicted Dropout Database](predicted_dropout.db).

**🔍 Why Use SQLite?**

- **High Compatibility**: Metabase supports SQLite as one of its data sources.  
- **Lightweight and Simple**: SQLite requires no server setup—just a `.db` file.  
- **Ideal for Prototypes or Small-Scale Deployments** such as local analytics dashboards.  
- **Portable**: The SQLite file can be used directly in Metabase without complex configuration.

2️⃣ **Run Metabase via Docker**

- Install Docker Desktop from the official site: [Docker Installation Guide](https://docs.docker.com/desktop/setup/install/windows-install/)  
- Open the Docker Terminal and create a folder named **metabase-data**:
  
  ```sh
  mkdir ~/metabase-share
  ```

3️⃣ Add the SQLite Database as a Data Source in Metabase

**Simply move the file [Predicted Dropout Database](predicted_dropout.db) into the `metabase-share` folder, and Metabase will be able to read the table contents and build dashboards directly.**

```sh
mv predicted_dropout.db ~/metabase-share/
```

4️⃣ Run the Metabase Service Using a Docker Container and Mount the Local Folder as a Volume

```sh
docker run -d -p 3000:3000 -v "C:\Users\ACER NITRO V15\metabase-share:/app/metabase-student" --name metabase_new metabase/metabase
```

**🔍 Code Explanation:**

1. `docker run`: Command to start a new container.  
2. `-d`: Runs the container in detached (background) mode.  
3. `-p 3000:3000`: Maps **port 3000** on the host machine to port 3000 in the container (Metabase runs on port 3000 by default).  
4. `-v "C:\Users\ACER NITRO V15\metabase-share:/app/metabase-student"`:  
   Mounts the local folder **(C:\Users\...)** into the container folder **(/app/metabase-student)** to share files such as the SQLite `.db` database.  
5. `--name metabase_new`: Names the container `metabase_new`.  
6. `metabase/metabase`: The official Metabase image from Docker Hub.

5️⃣ Access Metabase via your browser at **`http://localhost:3000/`**  
Then create an admin account, for example: _(Username: Tsamarah Abdullah, Password: Tsamarah192)_.  
Next, connect the database file located in your local folder  
`C:\Users\ACER_NITRO_V15\metabase-share\predicted_dropout.db`  
to the container path `/app/metabase-student/predicted_dropout.db`.

Or simply open the **Student Monitoring Dashboard** here:

![Student Monitoring Dashboard](muthiah_abdullah-dashboard.jpg)

## 📌Conclusion

---
Based on the feature importance evaluation from the optimized LightGBM model, several features were found to significantly influence the model’s decision in predicting whether a student is at risk of dropping out.

---

**✅ Most Influential Features:**

1️⃣ **Admission_grade**  
> Represents the student's entry-level grades — an indicator of initial academic readiness.

2️⃣ **Previous_qualification_grade**  
> Reflects grades from previous educational qualifications.

3️⃣ **Course**  
> The type or field of study.

4️⃣ **Mothers_occupation**  
> Mother's occupational background.

5️⃣ **Age_at_enrollment**  
> Age of the student at the time of enrollment.

6️⃣ **Approval_rate**  
> The ratio of passed courses to total enrolled units.

7️⃣ **Fathers_occupation**  
> Father's occupational background.

8️⃣ **Curricular_units_2nd_sem_grade**  
> Second semester grade performance.

9️⃣ **Curricular_units_2nd_sem_evaluations**  
> Number of evaluations completed in the second semester.

🔟 **Curricular_units_1st_sem_grade**  
> First semester grade performance.

### **👥 Common Characteristics of Students at Risk of Dropping Out:**

Based on the predictive model, students likely to drop out tend to have the following characteristics:

1️⃣ Students at risk generally have low admission grades, signaling a lack of initial academic preparedness.

2️⃣ They tend to have lower grades in their previous educational qualifications.

3️⃣ They often come from courses or study programs with high difficulty levels or misalignment with their personal interests.

4️⃣ Family background plays a role — especially when parents have occupations that offer limited economic or educational support.

5️⃣ Students who enroll at an older age also show a higher tendency to drop out, possibly due to additional responsibilities such as work or family.

6️⃣ Poor academic performance in the early semesters — including low grades or insufficient evaluations — serves as a strong indicator of potential dropout.

> This project successfully identified dropout risk using a machine learning model (LightGBM with SMOTE), achieving an accuracy of **90%**, and optimized the **prediction threshold** for more accurate results.

**The model reveals that student dropout potential is heavily influenced by a combination of academic factors (such as approved course units, GPA, and payment status) and personal factors (including age at enrollment, financial condition, and parental education background).**

---

## 💡Recommended Action Items

**✅ Below are several strategic steps that Jaya Jaya Institute can take:**

1. 🎯 **Intervention Based on Admission Grades**

   **Insight:** Students with low admission grades (`Admission_grade`) are highly vulnerable to dropping out.

   **Action:**  
   - Offer matriculation programs or additional academic support starting from the first semester.

2. 🧠 **Analysis Based on Academic History**

   **Insight:** Previous academic performance (`Previous_qualification_grade`) is also a key factor.

   **Action:**  
   - Identify students with low prior academic performance.  
   - Implement an early warning system based on initial semester performance.

3. 🧑‍🎓 **Evaluate Specific Study Programs**

   **Insight:** The `Course` feature is quite influential—certain programs may have higher dropout rates.

   **Action:**  
   - Conduct academic and psychosocial audits on departments with high dropout rates.  
   - Revise curricula, reduce stress levels, or adjust credit loads where necessary.

4. 👪 **Family Background**

   **Insight:** Parental occupation—especially the mother's—has a significant impact.

   **Action:**  
   - Provide financial or psychological support for students from vulnerable families.  
   - Offer scholarships based on socio-economic conditions.

5. 🎓 **Age and Adaptability**

   **Insight:** `Age_at_enrollment` affects dropout risk—likely due to adjustment challenges or family responsibilities.

   **Action:**  
   - Provide counseling services for non-traditional (older) students.  
   - Create cross-age peer learning groups.

6. 📉 **Early Academic Performance**

   **Insight:** Grades and evaluations in the 1st and 2nd semesters are critical indicators.

   **Action:**  
   - Implement a weekly academic performance monitoring system.  
   - Send alerts to academic advisors if student grades begin to decline.

---

📧 Feel free to contact me via [GitHub](https://github.com/MuthiahAinun) if you have any questions 😊.

---
