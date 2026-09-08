from langchain.tools import tool
from DummyDatas.MockData import MOCK_ACTIVITIES

@tool('activityLookUp')
def activityLookUp(destinationCity:str, category:str)->list:
    """Lookup for acitvities the given category"""
    """
    Args:
        destinationCity : City to lookup activity for
        category: categories of activity to lookup for
    Returns:
        List of activities in the ciy that are covered in the category 
    """
    filteredActivity = []
    for city, activities in MOCK_ACTIVITIES.items():
            if city.lower() != destinationCity.lower():
                continue 
            for activity in activities:
                if activity['category'] == category:
                    filteredActivity.append(activity)
    return filteredActivity
