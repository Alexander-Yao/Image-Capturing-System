using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Data
{
    public class GRepository<T> : IGenericRepository<T> where T : class
    {
            //private MapsVisionsDbContext _DbContext = null;
            private readonly MapsVisionsDbContext _DbContext;

            private DbSet<T> table = null;
            public GRepository()
            {
                //this._DbContext = new MapsVisionsDbContext();
                table = _DbContext.Set<T>();
            }
            public GRepository(MapsVisionsDbContext _DbContext)
            {
                this._DbContext = _DbContext;
                table = _DbContext.Set<T>();
            }
            public IEnumerable<T> GetAll()
            {
                return table.ToList();
            }
            public T GetById(object id)
            {
                return table.Find(id);
            }
            public void Insert(T obj)
            {
                table.Add(obj);
            }
            public void Update(T obj)
            {
                table.Attach(obj);
                _DbContext.Entry(obj).State = EntityState.Modified;
            }
            public void Delete(object id)
            {
                T existing = table.Find(id);
                table.Remove(existing);
            }
            public void Save()
            {
                _DbContext.SaveChanges();
            }
        }
    }
