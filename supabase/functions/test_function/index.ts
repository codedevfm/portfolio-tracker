import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const supabase = createClient(
  Deno.env.get('SUPABASE_URL') ?? '',
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
);

console.log("Test function starting up...");

Deno.serve(async (req) => {
  try {
    // You should use the anon key for most client-facing functions,
    // but the service role key is needed for privileged operations like this.
    // For a test, we will use the service role key to verify it is working.
    
    // Fetch all tables from the public schema
    const { data, error } = await supabase
      .from('pg_tables')
      .select('tablename')
      .eq('schemaname', 'public');

    if (error) {
      console.error('Error fetching schema:', error.message);
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    console.log('Successfully fetched schema data:', data);

    return new Response(JSON.stringify({
      message: 'Hello from your test Edge Function!',
      schema: data,
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('An unexpected error occurred:', err.message);
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});