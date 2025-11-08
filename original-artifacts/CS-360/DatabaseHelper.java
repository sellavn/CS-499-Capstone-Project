package com.example.project2vallesnicolas;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * Database helper class that manages all database operations for the Weight Tracker app.
 * Handles both user authentication and weight tracking data.
 */
public class DatabaseHelper extends SQLiteOpenHelper {

    // Database Info
    private static final String DATABASE_NAME = "WeightTracker.db";
    private static final int DATABASE_VERSION = 1;
    private static final String TAG = "DatabaseHelper";

    // Table Names
    private static final String TABLE_USERS = "users";
    private static final String TABLE_WEIGHT_ENTRIES = "weight_entries";

    // Common Column Names
    private static final String KEY_ID = "id";

    // Users Table Columns
    private static final String KEY_USER_USERNAME = "username";
    private static final String KEY_USER_EMAIL = "email";
    private static final String KEY_USER_PASSWORD = "password";

    // Weight Entries Table Columns
    private static final String KEY_WEIGHT_VALUE = "weight_value";
    private static final String KEY_WEIGHT_DATE = "date";
    private static final String KEY_WEIGHT_NOTES = "notes";
    private static final String KEY_WEIGHT_USER_ID = "user_id";

    // Date format for storing and retrieving dates
    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd", Locale.US);

    /**
     * Constructor for the DatabaseHelper
     * @param context The application context
     */
    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    /**
     * Called when the database is created for the first time.
     * Creates all necessary tables.
     */
    @Override
    public void onCreate(SQLiteDatabase db) {
        // Create Users table
        String CREATE_USERS_TABLE = "CREATE TABLE " + TABLE_USERS + "("
                + KEY_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
                + KEY_USER_USERNAME + " TEXT UNIQUE NOT NULL,"
                + KEY_USER_EMAIL + " TEXT,"
                + KEY_USER_PASSWORD + " TEXT NOT NULL"
                + ")";

        // Create Weight Entries table
        String CREATE_WEIGHT_ENTRIES_TABLE = "CREATE TABLE " + TABLE_WEIGHT_ENTRIES + "("
                + KEY_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
                + KEY_WEIGHT_VALUE + " REAL NOT NULL,"
                + KEY_WEIGHT_DATE + " TEXT NOT NULL,"
                + KEY_WEIGHT_NOTES + " TEXT,"
                + KEY_WEIGHT_USER_ID + " INTEGER,"
                + "FOREIGN KEY(" + KEY_WEIGHT_USER_ID + ") REFERENCES " + TABLE_USERS + "(" + KEY_ID + ")"
                + ")";

        // Execute the SQL statements
        db.execSQL(CREATE_USERS_TABLE);
        db.execSQL(CREATE_WEIGHT_ENTRIES_TABLE);

        Log.d(TAG, "Database tables created");
    }

    /**
     * Called when the database needs to be upgraded.
     * Handles dropping tables and recreating them.
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // Drop older tables if they exist
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_WEIGHT_ENTRIES);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_USERS);

        // Create tables again
        onCreate(db);
    }

    // ============== USER METHODS ============== //

    /**
     * Add a new user to the database
     * @param username The username of the new user
     * @param email The email of the new user (optional)
     * @param password The password of the new user
     * @return The ID of the newly created user, or -1 if creation failed
     */
    public long addUser(String username, String email, String password) {
        // Get writable database
        SQLiteDatabase db = this.getWritableDatabase();

        // Create ContentValues to add key/value pairs
        ContentValues values = new ContentValues();
        values.put(KEY_USER_USERNAME, username);
        values.put(KEY_USER_EMAIL, email);
        values.put(KEY_USER_PASSWORD, password);

        // Insert the row
        long userId = -1;
        try {
            userId = db.insertOrThrow(TABLE_USERS, null, values);
        } catch (Exception e) {
            Log.e(TAG, "Error creating user: " + e.getMessage());
        }

        // Close the database connection
        db.close();

        return userId;
    }

    /**
     * Verify a user's login credentials
     * @param username The username to check
     * @param password The password to verify
     * @return The user ID if credentials are valid, -1 otherwise
     */
    public long validateUser(String username, String password) {
        SQLiteDatabase db = this.getReadableDatabase();
        long userId = -1;

        String query = "SELECT " + KEY_ID + " FROM " + TABLE_USERS +
                " WHERE " + KEY_USER_USERNAME + " = ? AND " + KEY_USER_PASSWORD + " = ?";

        Cursor cursor = db.rawQuery(query, new String[]{username, password});

        if (cursor.moveToFirst()) {
            int idColumnIndex = cursor.getColumnIndex(KEY_ID);
            if (idColumnIndex != -1) {
                userId = cursor.getLong(idColumnIndex);
            }
        }

        cursor.close();
        db.close();

        return userId;
    }

    /**
     * Check if a username already exists in the database
     * @param username The username to check
     * @return true if the username exists, false otherwise
     */
    public boolean userExists(String username) {
        SQLiteDatabase db = this.getReadableDatabase();

        String query = "SELECT " + KEY_ID + " FROM " + TABLE_USERS +
                " WHERE " + KEY_USER_USERNAME + " = ?";

        Cursor cursor = db.rawQuery(query, new String[]{username});

        boolean exists = cursor.getCount() > 0;

        cursor.close();
        db.close();

        return exists;
    }

    // ============== WEIGHT ENTRY METHODS ============== //

    /**
     * Add a new weight entry to the database
     * @param weight The weight value
     * @param date The date of the entry
     * @param notes Optional notes about the entry
     * @param userId The ID of the user making the entry
     * @return The ID of the newly created entry, or -1 if creation failed
     */
    public long addWeightEntry(float weight, Date date, String notes, long userId) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_WEIGHT_VALUE, weight);
        values.put(KEY_WEIGHT_DATE, DATE_FORMAT.format(date));
        values.put(KEY_WEIGHT_NOTES, notes);
        values.put(KEY_WEIGHT_USER_ID, userId);

        long entryId = -1;
        try {
            entryId = db.insertOrThrow(TABLE_WEIGHT_ENTRIES, null, values);
        } catch (Exception e) {
            Log.e(TAG, "Error adding weight entry: " + e.getMessage());
        }

        db.close();

        return entryId;
    }

    /**
     * Update an existing weight entry
     * @param entryId The ID of the entry to update
     * @param weight The new weight value
     * @param date The new date
     * @param notes The new notes
     * @return true if update was successful, false otherwise
     */
    public boolean updateWeightEntry(long entryId, float weight, Date date, String notes) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_WEIGHT_VALUE, weight);
        values.put(KEY_WEIGHT_DATE, DATE_FORMAT.format(date));
        values.put(KEY_WEIGHT_NOTES, notes);

        int rowsAffected = db.update(TABLE_WEIGHT_ENTRIES, values,
                KEY_ID + " = ?", new String[]{String.valueOf(entryId)});

        db.close();

        return rowsAffected > 0;
    }

    /**
     * Delete a weight entry from the database
     * @param entryId The ID of the entry to delete
     * @return true if deletion was successful, false otherwise
     */
    public boolean deleteWeightEntry(long entryId) {
        SQLiteDatabase db = this.getWritableDatabase();

        int rowsAffected = db.delete(TABLE_WEIGHT_ENTRIES,
                KEY_ID + " = ?", new String[]{String.valueOf(entryId)});

        db.close();

        return rowsAffected > 0;
    }

    /**
     * Retrieve all weight entries for a specific user
     * @param userId The ID of the user
     * @return A list of WeightEntry objects
     */
    public List<WeightEntry> getAllWeightEntries(long userId) {
        List<WeightEntry> weightEntries = new ArrayList<>();

        SQLiteDatabase db = this.getReadableDatabase();

        String query = "SELECT * FROM " + TABLE_WEIGHT_ENTRIES +
                " WHERE " + KEY_WEIGHT_USER_ID + " = ?" +
                " ORDER BY " + KEY_WEIGHT_DATE + " DESC";

        Cursor cursor = db.rawQuery(query, new String[]{String.valueOf(userId)});

        try {
            if (cursor.moveToFirst()) {
                do {
                    WeightEntry entry = new WeightEntry();

                    int idIndex = cursor.getColumnIndex(KEY_ID);
                    if (idIndex != -1) {
                        entry.setId(cursor.getLong(idIndex));
                    }

                    int weightIndex = cursor.getColumnIndex(KEY_WEIGHT_VALUE);
                    if (weightIndex != -1) {
                        entry.setWeight(cursor.getFloat(weightIndex));
                    }

                    // Parse the date
                    int dateIndex = cursor.getColumnIndex(KEY_WEIGHT_DATE);
                    if (dateIndex != -1) {
                        String dateStr = cursor.getString(dateIndex);
                        try {
                            entry.setDate(DATE_FORMAT.parse(dateStr));
                        } catch (ParseException e) {
                            Log.e(TAG, "Error parsing date: " + e.getMessage());
                            entry.setDate(new Date()); // Default to current date if parsing fails
                        }
                    } else {
                        entry.setDate(new Date()); // Default to current date if column not found
                    }

                    int notesIndex = cursor.getColumnIndex(KEY_WEIGHT_NOTES);
                    if (notesIndex != -1) {
                        entry.setNotes(cursor.getString(notesIndex));
                    }

                    int userIdIndex = cursor.getColumnIndex(KEY_WEIGHT_USER_ID);
                    if (userIdIndex != -1) {
                        entry.setUserId(cursor.getLong(userIdIndex));
                    }

                    weightEntries.add(entry);
                } while (cursor.moveToNext());
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting weight entries: " + e.getMessage());
        } finally {
            if (cursor != null && !cursor.isClosed()) {
                cursor.close();
            }
        }

        db.close();

        return weightEntries;
    }

    /**
     * Get the most recent weight entry for a user
     * @param userId The ID of the user
     * @return The most recent WeightEntry, or null if none exists
     */
    public WeightEntry getLatestWeightEntry(long userId) {
        WeightEntry entry = null;

        SQLiteDatabase db = this.getReadableDatabase();

        String query = "SELECT * FROM " + TABLE_WEIGHT_ENTRIES +
                " WHERE " + KEY_WEIGHT_USER_ID + " = ?" +
                " ORDER BY " + KEY_WEIGHT_DATE + " DESC LIMIT 1";

        Cursor cursor = db.rawQuery(query, new String[]{String.valueOf(userId)});

        try {
            if (cursor.moveToFirst()) {
                entry = new WeightEntry();

                int idIndex = cursor.getColumnIndex(KEY_ID);
                if (idIndex != -1) {
                    entry.setId(cursor.getLong(idIndex));
                }

                int weightIndex = cursor.getColumnIndex(KEY_WEIGHT_VALUE);
                if (weightIndex != -1) {
                    entry.setWeight(cursor.getFloat(weightIndex));
                }

                // Parse the date
                int dateIndex = cursor.getColumnIndex(KEY_WEIGHT_DATE);
                if (dateIndex != -1) {
                    String dateStr = cursor.getString(dateIndex);
                    try {
                        entry.setDate(DATE_FORMAT.parse(dateStr));
                    } catch (ParseException e) {
                        Log.e(TAG, "Error parsing date: " + e.getMessage());
                        entry.setDate(new Date()); // Default to current date if parsing fails
                    }
                } else {
                    entry.setDate(new Date()); // Default to current date if column not found
                }

                int notesIndex = cursor.getColumnIndex(KEY_WEIGHT_NOTES);
                if (notesIndex != -1) {
                    entry.setNotes(cursor.getString(notesIndex));
                }

                int userIdIndex = cursor.getColumnIndex(KEY_WEIGHT_USER_ID);
                if (userIdIndex != -1) {
                    entry.setUserId(cursor.getLong(userIdIndex));
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting latest weight entry: " + e.getMessage());
        } finally {
            if (cursor != null && !cursor.isClosed()) {
                cursor.close();
            }
        }

        db.close();

        return entry;
    }

    /**
     * Delete all weight entries for a specific user
     * @param userId The ID of the user
     * @return true if all entries were deleted successfully, false otherwise
     */
    public boolean deleteAllWeightEntries(long userId) {
        SQLiteDatabase db = this.getWritableDatabase();

        int rowsDeleted = db.delete(
                TABLE_WEIGHT_ENTRIES,
                KEY_WEIGHT_USER_ID + " = ?",
                new String[]{String.valueOf(userId)});

        db.close();

        // Return true if at least one row was deleted or if there were no entries to delete
        return rowsDeleted >= 0;
    }

    /**
     * Delete a user account from the database
     * @param userId The ID of the user to delete
     * @return true if the user was deleted successfully, false otherwise
     */
    public boolean deleteUser(long userId) {
        SQLiteDatabase db = this.getWritableDatabase();

        int rowsDeleted = db.delete(
                TABLE_USERS,
                KEY_ID + " = ?",
                new String[]{String.valueOf(userId)});

        db.close();

        return rowsDeleted > 0;
    }

}