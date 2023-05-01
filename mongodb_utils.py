import pymongo

# Set up the MongoDB client and database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["academicworld"]

# Define the aggregation pipeline
pipeline = [
    { "$match": { "year": { "$gte": 2012 } } },
    { "$unwind": "$keywords" },
    {
        "$group": {
            "_id": "$keywords.name",
            "count": { "$sum": 1 }
        }
    },
    { "$sort": { "count": -1 } },
    {
        "$project": {
            "_id": 0,
            "keyword": "$_id",
            "count": 1
        }
    }
]

def getkeywords():
    pipeline_result = db.publications.aggregate(pipeline)
    result = []
    for doc in pipeline_result:
        result.append({
            'Keyword': doc['keyword'],
            'Count': doc['count']
        })
    return result


"""
Find the top-10 most popular keywords among publications that were published in or after 2012.
For this question, we consider a publication relevant to a keyword if it has the keyword (regardless of the score).
A keyword is more popular if more publications are relevant to it.
Return the name of keywords and the number of relevant publications.
You may assume that the keyword name is unique for each keyword.
 Order the results by the descending order of the publication numbers of each keyword.


db.publications.aggregate([
    {
        $match: { "year": { $gte: 2012 } }
    },
    {
        $unwind: "$keywords"
    },
    {
        $group: {
            _id: "$keywords.name",
            count: { $sum: 1 }
        }
    },
    {
        $sort: { "count": -1 }
    },
    {
        $limit: 10
    },
    {
        $project: {
            _id: 0,
            keyword: "$_id",
            count: 1
        }
    }
])
"""