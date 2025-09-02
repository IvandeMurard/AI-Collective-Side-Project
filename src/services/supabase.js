import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);

// Upload video file to Supabase Storage
export const uploadVideo = async (file, fileName) => {
  try {
    const { data, error } = await supabase.storage
      .from('avatar-videos')
      .upload(`videos/${fileName}`, file, {
        cacheControl: '3600',
        upsert: false
      });

    if (error) throw error;

    // Get public URL
    const { data: { publicUrl } } = supabase.storage
      .from('avatar-videos')
      .getPublicUrl(`videos/${fileName}`);

    return publicUrl;
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
};

// Save profile to Supabase Database
export const saveProfile = async (profile) => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .insert([profile])
      .select();

    if (error) throw error;
    return data[0];
  } catch (error) {
    console.error('Error saving profile:', error);
    throw error;
  }
};

// Get all profiles from Supabase
export const getProfiles = async () => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  } catch (error) {
    console.error('Error fetching profiles:', error);
    throw error;
  }
};
