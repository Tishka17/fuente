* Error = Skip Field (certain field is treated as Absent, others are processed)

| src1      | src 2     | First() | Last()  | Unite() |
|-----------|-----------|---------|---------|---------|
| ✅ Good    | ✅ Good    | 1       | 2       | unite   |
| ✅ Good    | Absent    | 1       | 1       | 1       |
| ✅ Good    | ❌ Invalid | 1       | 1       | 1       |
| Absent    | ✅ Good    | 2       | 2       | 2       |
| Absent    | Absent    | default | default | default |
| Absent    | ❌ Invalid | default | default | default |
| ❌ Invalid | ✅ Good    | 2       | 2       | 2       |
| ❌ Invalid | Absent    | default | default | default |
| ❌ Invalid | ❌ Invalid | default | default | default |

* Error = Skip Source (the whould source is not processed as it was not configured)

* Error = Fail Not Parsed (if only invalid values found, raise and error)

| src1      | src 2     | First() | Last()  | Unite() |
|-----------|-----------|---------|---------|---------|
| ✅ Good    | ✅ Good    | 1       | 2       | unite   |
| ✅ Good    | Absent    | 1       | 1       | 1       |
| ✅ Good    | ❌ Invalid | 1       | 1       | 1       |
| Absent    | ✅ Good    | 2       | 2       | 2       |
| Absent    | Absent    | default | default | default |
| Absent    | ❌ Invalid | fail    | fail    | fail    |
| ❌ Invalid | ✅ Good    | 2       | 2       | 2       |
| ❌ Invalid | Absent    | fail    | fail    | fail    |
| ❌ Invalid | ❌ Invalid | fail    | fail    | fail    |

* Error = Fail Always (raise and error if there is invalid value regardless merge strategy)

| src1      | src 2     | First() | Last()  | Unite() |
|-----------|-----------|---------|---------|---------|
| ✅ Good    | ✅ Good    | 1       | 2       | unite   |
| ✅ Good    | Absent    | 1       | 1       | 1       |
| ✅ Good    | ❌ Invalid | fail    | fail    | fail    |
| Absent    | ✅ Good    | 2       | 2       | 2       |
| Absent    | Absent    | default | default | default |
| Absent    | ❌ Invalid | fail    | fail    | fail    |
| ❌ Invalid | ✅ Good    | fail    | fail    | fail    |
| ❌ Invalid | Absent    | fail    | fail    | fail    |
| ❌ Invalid | ❌ Invalid | fail    | fail    | fail    |

