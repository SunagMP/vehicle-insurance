from fastapi import FastAPI
from pydantic import computed_field, BaseModel, Field
from typing import Literal, Optional, Annotated

import pandas as pd
import pickle

app = FastAPI()

#------------------- creating the input schema
class input_schema(BaseModel):
    gender : Annotated[Literal['Male', 'Female'], Field(description="Gender of the vehicle owner", examples=['Male', 'Female'])]
    age : Annotated[int, Field(description="self.vehicle_age of the vehicle owner", examples=[34, 54], gt=0, lt=120)]
    driving_license : Annotated[Literal[0, 1], Field(description="whether person has DL or not , if yes 1 else 0", examples=[0, 1])]
    previously_insured : Annotated[Literal[0, 1], Field(descrption="Whether the vehicle already insured if yes 1, else 0")]
    vehicle_age : Annotated[Literal["1-2 Year", "< 1 Year", "> 2 Year"], Field(description="vehicle self.vehicle_age in years", examples=["1-2 Year", "< 1 Year", "> 2 Year"])]
    vehicle_damage : Annotated[Literal['Yes', 'No'], Field(description="is vehicle to insure is damaged if yes 1, else 0", examples=['Yes', 'No'])]
    annual_premium : Annotated[float, Field(description="the annual premium self.amount spending on the vehicle", examples=[2630, 2546.23])]
    policy_sales_channel : Annotated[float, Field(description="policy sales channel", examples=[157, 152])]
    vintage : Annotated[int, Field(description="vintage of the insurance", examples=[260, 296])]

    @computed_field
    @property
    def age_group(self) -> int:
        if self.age>=0 and self.age<=30:
            return 0
        elif self.age>=31 and self.age<=50:
            return 1
        return 2
    
    @computed_field
    @property
    def premium_range(self) -> int:
        if self.annual_premium>0 and self.annual_premium<=50000:
            return 0
        elif self.annual_premium>=50001 and self.annual_premium<=150000:
            return 1
        return 2

    @computed_field
    @property
    def v_age(self) -> int:
        if self.vehicle_age == "1-2 Year":
            return 0 
        elif self.vehicle_age == "< 1 Year": 
            return 1
        return 2
    
    @computed_field
    @property
    def old_damaged_vehicle(self) -> int:
        if (self.vehicle_age == '> 2 Years') and (self.vehicle_age == "Yes"):
            return 1
        return 0
    
    @computed_field
    @property
    def premium_per_vintage(self) -> float:
        return (self.annual_premium)/(self.vintage)

    

@app.get("/")
def home_page():
    return {"message":"You are on the home page of the vehicle insurance predictor"}


"""
"the input given is ": {
    "age": 34,
    "vehicle_age": "1-2 Year",
    "annual_premium": 2630,
    "premium_per_vintage": 10.115384615384615
  }							
"""
@app.post("/predict")
def predict(input:input_schema):
    input_df = pd.DataFrame([{
        'Gender' : input.gender,
        'Driving_License' : input.driving_license,
        'Previously_Insured' : input.previously_insured,
        'Vehicle_Age' : input.v_age,
        'Vehicle_Damage' : input.vehicle_damage,
        'Policy_Sales_Channel' : input.policy_sales_channel,
        'Vintage' : input.vintage,
        'Age_Group' : input.age_group,
        'Old_Damaged_vehicle' : input.old_damaged_vehicle,
        'Premium_Range' : input.premium_range,
        'Premium_Per_Vintage' : input.premium_per_vintage
    }])

    with open('models/model.pkl', 'rb') as f:
        trained_model = pickle.load(f)

    y_pred = trained_model.predict(input_df)
    prediction = int(y_pred[0])

    return {"Vehicle insurance prediction ": prediction}
