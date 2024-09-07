from .supabase import supabase

def create_record(table: str, data: dict):
    response = supabase.table(table).insert(data).execute()
    return response.data

def read_records(table: str, filters: dict = None):
    query = supabase.table(table).select("*")
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
        
    response = query.execute()
    return response.data

def update_record(table: str, filters: dict, updates: dict):
    query = supabase.table(table)
    for key, value in filters.items():
        query = query.eq(key, value)
    
    response = query.update(updates).execute()
    return response.data

def delete_record(table: str, filters: dict):
    query = supabase.table(table)
    for key, value in filters.items():
        query = query.eq(key, value)
    
    response = query.delete().execute()
    return response.data
