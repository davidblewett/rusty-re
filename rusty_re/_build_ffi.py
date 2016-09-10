from cffi import FFI

ffi = FFI()
ffi.set_source('rusty_re._ffi', None)
ffi.cdef("""
    /** ===============================
                   Utility
        =============================== **/

    typedef struct {
        bool  has_error;
        char* error_type;
        char* error_description;
        char* error_display;
        char* error_debug;
    } Context;

    Context* regex_context_new();

    void regex_context_free(Context*);
    void regex_string_free(char*);

    /** ===============================
                     Regex
        =============================== **/

    typedef struct Regex Regex;
    typedef struct {
        int32_t start, end;
    } FindResult;

    Regex* regex_new(Context*, char*);
    void regex_free(Regex*);

    bool regex_is_match(Regex*, char*);

    FindResult regex_find(Regex*, char*);
    void regex_findresult_free(FindResult);

    /** ===============================
                     Set
        ===============================

    typedef struct FileSetBuilder FileSetBuilder;
    typedef struct MemSetBuilder MemSetBuilder;
    typedef struct Set Set;
    typedef struct SetStream SetStream;
    typedef struct SetLevStream SetLevStream;
    typedef struct SetRegexStream SetRegexStream;
    typedef struct SetOpBuilder SetOpBuilder;
    typedef struct SetUnion SetUnion;
    typedef struct SetIntersection SetIntersection;
    typedef struct SetDifference SetDifference;
    typedef struct SetSymmetricDifference SetSymmetricDifference;
    typedef struct SetStreamBuilder SetStreamBuilder;

    FileSetBuilder* fst_filesetbuilder_new(Context*, BufWriter*);
    void fst_filesetbuilder_insert(Context*, FileSetBuilder*, char*);
    void fst_filesetbuilder_finish(Context*, FileSetBuilder*);

    MemSetBuilder* fst_memsetbuilder_new();
    bool fst_memsetbuilder_insert(Context*, MemSetBuilder*, char*);
    Set* fst_memsetbuilder_finish(Context*, MemSetBuilder*);

    Set* fst_set_open(Context*, char*);
    bool fst_set_contains(Set*, char*);
    size_t fst_set_len(Set*);
    bool fst_set_isdisjoint(Set*, Set*);
    bool fst_set_issubset(Set*, Set*);
    bool fst_set_issuperset(Set*, Set*);
    SetStream* fst_set_stream(Set*);
    SetLevStream* fst_set_levsearch(Set*, Levenshtein*);
    SetRegexStream* fst_set_regexsearch(Set*, Regex*);
    SetOpBuilder* fst_set_make_opbuilder(Set*);
    void fst_set_free(Set*);

    char* fst_set_stream_next(SetStream*);
    void fst_set_stream_free(SetStream*);

    char* fst_set_levstream_next(SetLevStream*);
    void fst_set_levstream_free(SetLevStream*);

    char* fst_set_regexstream_next(SetRegexStream*);
    void fst_set_regexstream_free(SetRegexStream*);

    void fst_set_opbuilder_push(SetOpBuilder*, Set*);
    void fst_set_opbuilder_free(SetOpBuilder*);
    SetUnion* fst_set_opbuilder_union(SetOpBuilder*);
    SetIntersection* fst_set_opbuilder_intersection(SetOpBuilder*);
    SetDifference* fst_set_opbuilder_difference(SetOpBuilder*);
    SetSymmetricDifference* fst_set_opbuilder_symmetricdifference(
        SetOpBuilder*);

    char* fst_set_union_next(SetUnion*);
    void fst_set_union_free(SetUnion*);

    char* fst_set_intersection_next(SetIntersection*);
    void fst_set_intersection_free(SetIntersection*);

    char* fst_set_difference_next(SetDifference*);
    void fst_set_difference_free(SetDifference*);

    char* fst_set_symmetricdifference_next(SetSymmetricDifference*);
    void fst_set_symmetricdifference_free(SetSymmetricDifference*);

    SetStreamBuilder* fst_set_streambuilder_new(Set*);
    SetStreamBuilder* fst_set_streambuilder_add_ge(SetStreamBuilder*, char*);
    SetStreamBuilder* fst_set_streambuilder_add_lt(SetStreamBuilder*, char*);
    SetStream* fst_set_streambuilder_finish(SetStreamBuilder*);

 **/

""")

if __name__ == '__main__':
    ffi.compile()
